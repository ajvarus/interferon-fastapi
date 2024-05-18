
import os
from typing import TypeVar, Type, Optional

from datetime import datetime, timezone, timedelta
import jwt
import jwt.exceptions
import uuid

from models.types import  InterferonUser, JWTPayload, UserSession

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
            if user_session and await cls._store_session(session=user_session):
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
            user_session.last_active = now.timestamp()

            jwt_payload: JWTPayload = await JWTPayload.from_user_session(user_session)
            user_session.token = await cls._generate_jwt(payload=jwt_payload)

            return user_session
        except Exception as e:
            print(str(e))


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
   
    # def verify_jwt(self, token: str) -> bool:
    #     try:
    #         payload: JWTToken = JWTToken(**jwt.decode(
    #             jwt = token,
    #             key = str(os.environ.get("SECRET_KEY")),
    #             algorithms = [os.environ.get("ALGORITHM", "HS256")]
    #         ))
    #         return payload.sub == self.user.user_id
    #     except jwt.exceptions.PyJWTError as e:
    #         print(str(e))
    #         return False

    # def terminate_session(self):
    #     self.user.is_active = False
    #     self.user.token = None

    # def refresh_session(self):
    #     self.last_active = datetime.now(timezone.utc)
    #     self.user.is_active = True
    #     self.user.token = self.generate_jwt()

    # @staticmethod
    # def is_session_active(session: Type[T]) -> bool:
    #     return session.user.is_active and (datetime.now(timezone.utc) - session.user.last_active).seconds < 3600
    

# import asyncio
# async def test_login():
#     user = InterferonUser(
#     user_id="4",
#     token=None,
#     supabase_token="234",
#     is_active=True,
#     last_active=None
#     )
#     r: Redis = await RedisManager.get_client()
#     session_engine: UserSessionEngine = UserSessionEngine(r=r)
#     user_session = await session_engine.start_session(user=user)
#     print("Finished")
#     print(user_session)

# asyncio.run(test_login())