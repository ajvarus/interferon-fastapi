
import os
from typing import TypeVar, Type, Optional

from datetime import datetime, timezone, timedelta
import jwt
import jwt.exceptions
import uuid
import json

import redis.exceptions

from models.types import  InterferonUser, JWTPayload, UserSession

import redis
from redis.asyncio import Redis
from redised import RedisManager


T = TypeVar("T", bound="UserSessionEngine")

class UserSessionEngine:

    _instance: Type[T] = None
    _r: Redis = None


    def __new__(cls, r: Redis) -> Type[T]:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._r = r
        return cls._instance

    @classmethod
    async def start_session(cls, user: InterferonUser) -> UserSession:
        if await cls._valid_for_creation(user=user):
            user_session = await cls._create_session(user=user)
            if user_session.user_id and await cls._store_session(session=user_session):
                return user_session
        return UserSession()

    @classmethod
    async def _store_session(cls, session: UserSession) -> bool:
        try:
            async with cls._r.pipeline() as pipe:
                await (pipe
                       .lpush(session.user_id, session.session_id)
                       .setex(session.session_id, timedelta(days=1), session.model_dump_json())
                       .execute())
            return True
        except Exception as e:
            print(str(e))
            return False
        


    @classmethod
    async def _create_session(cls, user: InterferonUser) -> UserSession:
        try:
            user_session: UserSession = await UserSession.from_user(user=user)
            user_session.session_id = str(uuid.uuid4())

            now: datetime = datetime.now(timezone.utc)
            user_session.expiry = (now + timedelta(days=1)).timestamp()
            #user_session.expiry = (now + timedelta(seconds=1)).timestamp()
            user_session.last_active = now.timestamp()

            jwt_payload: JWTPayload = await JWTPayload.from_user_session(user_session)
            user_session.token = await cls._generate_jwt(payload=jwt_payload)

            return user_session
        except Exception as e:
            print(str(e))
            return UserSession()


    @classmethod
    async def _valid_for_creation(cls, user: InterferonUser) -> bool:
        is_default_user = user.model_dump() == InterferonUser().model_dump()
        has_user_id = user.user_id is not None
        # Below variable is used to allow only one active user session.
        has_active_session = await cls._r.exists(user.user_id) > 0
        
        if not is_default_user and has_user_id and not has_active_session: 
            return True
        return False


    @classmethod
    async def _generate_jwt(cls, payload: JWTPayload) -> str:
        return jwt.encode(
            payload = payload.model_dump(),
            key = str(os.environ.get("SECRET_KEY")),
            algorithm = os.environ.get("ALGORITHM", "HS256")
        )
    
    @classmethod
    async def verify_and_retrieve_session(cls, token: str) -> UserSession:
        try:
            is_valid_session, payload = cls._verify_session(token)
            if not payload.is_default():
                user_id: str = payload.sub
                session_id: str = payload.ssn
                session: UserSession = await cls._retrieve_session(user_id=user_id, session_id=session_id)
                if not session.is_default():
                    if is_valid_session:
                        updated_session: UserSession = await cls._update_session(session=session)
                        return updated_session
                    else:
                        deleted_session: UserSession = await cls._delete_session(user_id, session_id)
                        return deleted_session 
                else: return UserSession()    
            else: return UserSession()     
        except Exception as e:
            print(str(e))
            return UserSession()


    @classmethod
    def _verify_session(cls, token: str) -> tuple[bool, JWTPayload]:
        payload: JWTPayload = JWTPayload()
        is_valid: bool = False
        try:
            payload: JWTPayload = JWTPayload(**jwt.decode(
            jwt = token,
            key = str(os.environ.get("SECRET_KEY")),
            algorithms = [os.environ.get("ALGORITHM", "HS256")],
            options = {"verify_signature": False}
            ))
            if not payload.is_default():
                is_valid = cls._validate_session(exp=payload.exp)
            return is_valid, payload
        except (jwt.InvalidTokenError, jwt.exceptions.PyJWTError) as e:
            print(str(e))
            return is_valid, payload
        

    @classmethod    
    async def _update_session(cls, session: UserSession) -> UserSession:
        now: float = datetime.now(timezone.utc).timestamp()
        session_dict: dict = session.model_dump()
        session_dict.update({"last_active": now})
        await cls._r.set(session.session_id, json.dumps(session_dict))
        session.last_active = now
        session.is_active = True
        return session

    @classmethod
    async def _delete_session(cls, user_id: str, session_id: str) -> UserSession:
        try:
            if (await cls._r.exists(session_id)) and (await cls._r.exists(user_id)):
                await cls._r.delete(session_id)
                await cls._r.lrem(user_id, 0, session_id)
                return UserSession(user_id=user_id, session_id=session_id, is_active=False)
                # is_list_empty = await cls._r.llen(user_id) == 0
                # if is_list_empty:
                #     await cls._r.delete(user_id)
            else:
                return UserSession()  
        except redis.RedisError as e:
            return UserSession()
        
    @classmethod
    async def _retrieve_session(cls, user_id: str, session_id: str) -> UserSession:
        try:
            if await cls._r.exists(user_id) == 1:
                is_retrievable: bool = await cls._r.llen(user_id) == 1
                if is_retrievable:
                    sessions: list = await cls._r.lrange(user_id, 0, -1)
                    if session_id.encode() in sessions:
                        session: dict = json.loads((await cls._r.get(session_id)).decode())
                        if session:
                            return UserSession(**session)
                    return UserSession(is_active=False)
                return UserSession(is_active=False)
            return UserSession()
        except (redis.exceptions.RedisError, Exception) as e:
            print(str(e))
            return UserSession()
        
    @classmethod
    def _validate_session(cls, exp: int) -> bool:
        expiry_time: datetime = datetime.fromtimestamp(exp, timezone.utc)
        is_valid: bool = datetime.now(timezone.utc) < expiry_time
        return is_valid

    @classmethod
    async def terminate_session(cls, token: str) -> UserSession:
        payload: JWTPayload
        session: UserSession = UserSession()
        _, payload = cls._verify_session(token)
        if not payload.is_default():
            session: UserSession = await cls._delete_session(user_id=payload.sub,
                                                             session_id=payload.ssn)
            # if not session.is_default():
            #     return session
        return session

    # def refresh_session(self):
    #     self.last_active = datetime.now(timezone.utc)
    #     self.user.is_active = True
    #     self.user.token = self.generate_jwt()


    

# import asyncio
# async def test_login():
#     r: Redis = await RedisManager.get_client()
#     session_engine: UserSessionEngine = UserSessionEngine(r=r)

    # user = InterferonUser(
    # user_id="11",
    # token=None,
    # supabase_token="234",
    # is_active=True,
    # last_active=None
    # )
    # user_session = await session_engine.start_session(user=user)
    # print("Finished")
    # print(user_session)

    # jwt: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMSIsImV4cCI6MTcxNjIyNTM4NywiaWF0IjoxNzE2MTM4OTg3LCJzc24iOiI1MTk4OTUyMS0yNDZhLTRiNzItYmU5YS00ZTk1ZWU3NDMwYmIifQ.MzY6nXGqG9CJyvak63XCxAK9Wh81x7ZbsTnE6Nxv-yo"
    # user_session = await session_engine.verify_and_retrieve_session(token=jwt)
    # print("Verified")
    # print(user_session)

#     jwt: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMSIsImV4cCI6MTcxNjIyNTM4NywiaWF0IjoxNzE2MTM4OTg3LCJzc24iOiI1MTk4OTUyMS0yNDZhLTRiNzItYmU5YS00ZTk1ZWU3NDMwYmIifQ.MzY6nXGqG9CJyvak63XCxAK9Wh81x7ZbsTnE6Nxv-yo"
#     user_session = await session_engine.terminate_session(token=jwt)
#     print("Terminated")
#     print(user_session)

# asyncio.run(test_login())