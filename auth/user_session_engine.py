# /auth/user_session_engine.py

import os
from typing import Optional, TypeVar, Type, List, cast

from datetime import datetime, timezone, timedelta
import jwt
import jwt.exceptions
import uuid
import json

import redis.exceptions

from models.types import InterferonUser, JWTPayload, UserSession

import redis
from redis.asyncio import Redis

from errors.types import SessionError
from errors.error_codes import SessionErrorCode as sec


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
        try:
            if await cls._valid_for_creation(user=user):
                user_session = await cls._create_session(user=user)
                if user_session.user_id and await cls._store_session(
                    session=user_session
                ):
                    return user_session
            return UserSession()
        except SessionError as e:
            raise e
        except Exception as e:
            return UserSession()

    @classmethod
    async def _store_session(cls, session: UserSession) -> bool:
        try:
            async with cls._r.pipeline() as pipe:
                await (
                    pipe.lpush(session.user_id, session.session_id)
                    .setex(
                        session.session_id, timedelta(days=1), session.model_dump_json()
                    )
                    .execute()
                )
            return True
        except Exception as e:
            print(str(e))
            return False

    @classmethod
    async def _create_session(cls, user: InterferonUser) -> UserSession:
        try:
            user_session: UserSession = UserSession.from_user(user=user)
            user_session.session_id = str(uuid.uuid4())

            now: datetime = datetime.now(timezone.utc)
            user_session.expiry = (now + timedelta(days=1)).timestamp()
            # user_session.expiry = (now + timedelta(seconds=1)).timestamp()
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
        has_active_session: bool = await cls._r.exists(user.user_id) > 0

        if has_active_session:
            raise SessionError(sec.SESSION_ALREADY_EXISTS)
        if not is_default_user and has_user_id and not has_active_session:
            return True
        return False

    @classmethod
    async def _generate_jwt(cls, payload: JWTPayload) -> str:
        return jwt.encode(
            payload=payload.model_dump(),
            key=str(os.environ.get("SECRET_KEY")),
            algorithm=os.environ.get("ALGORITHM", "HS256"),
        )

    @classmethod
    async def verify_and_retrieve_session(cls, token: str) -> UserSession:
        try:
            is_valid_session, payload = cls._verify_session(token)
            if not payload.is_default():
                user_id: str = payload.sub
                session_id: str = payload.ssn
                session: UserSession = await cls._retrieve_session(
                    user_id=user_id, session_id=session_id
                )
                if not session.is_default():
                    if is_valid_session:
                        updated_session: UserSession = await cls._update_session(
                            session=session
                        )
                        return updated_session
                    else:
                        deleted_session: UserSession = await cls._delete_session(
                            user_id, session_id
                        )
                        deleted_session.supabase_token = session.supabase_token
                        return deleted_session
                else:
                    return UserSession()
            else:
                return UserSession()
        except Exception as e:
            print(str(e))
            return UserSession()

    @classmethod
    def _verify_session(cls, token: str) -> tuple[bool, JWTPayload]:
        payload: JWTPayload = JWTPayload()
        is_valid: bool = False
        try:
            payload: JWTPayload = JWTPayload(
                **jwt.decode(
                    jwt=token,
                    key=str(os.environ.get("SECRET_KEY")),
                    algorithms=[os.environ.get("ALGORITHM", "HS256")],
                    options={"verify_signature": False},
                )
            )
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
                if await cls._cleanup_session(user_id):
                    return UserSession(
                        user_id=user_id, session_id=session_id, is_active=False
                    )
                else:
                    return UserSession()
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
                        session: dict = json.loads(
                            (await cls._r.get(session_id)).decode()
                        )
                        if session:
                            return UserSession(**session)
                    return UserSession(is_active=False)
                return UserSession(is_active=False)
            return UserSession()
        except (redis.exceptions.RedisError, Exception) as e:
            print(str(e))
            return UserSession()

    @classmethod
    # type: ignore
    async def force_terminate_all_sessions(cls, user_id: str) -> bool:
        try:
            if not await cls._r.exists(user_id):  # type: ignore
                return False

            session_ids: List[bytes] = await cls._r.lrange(user_id, 0, -1)  # type: ignore

            async with cls._r.pipeline(transaction=True) as pipe:
                for session_id in session_ids:
                    pipe.delete(session_id)
                pipe.delete(user_id)
                await pipe.execute()

            # for session_id in session_ids:
            #     _ = await cls._r.delete(session_id)

            # _ = await cls._r.delete(user_id)
            _ = await cls._cleanup_session(user_id)

            return True
        except Exception:
            return False

    @classmethod
    def _validate_session(cls, exp: int) -> bool:
        expiry_time: datetime = datetime.fromtimestamp(exp, timezone.utc)
        is_valid: bool = datetime.now(timezone.utc) < expiry_time
        return is_valid

    @classmethod
    async def _cleanup_session(cls, user_id: str) -> bool:
        try:
            redis_key: str = f"{user_id}:*"
            # Exclude master key.
            exclude_key: str = f"{user_id}:master_key"
            redis_cursor = b"0"
            keys_to_delete: List[str] = []
            while redis_cursor:
                redis_cursor, keys = await cls._r.scan(redis_cursor, match=redis_key)
                keys_to_delete.extend([key.decode() for key in keys])
            if keys_to_delete:
                # Exclude master key deletion - Unexpected behavior if deleted.
                keys_to_delete = [key for key in keys_to_delete if key != exclude_key]
                await cls._r.delete(*keys_to_delete)
            return True
        except:
            return False

    @classmethod
    async def terminate_session(cls, token: str) -> UserSession:
        payload: JWTPayload = JWTPayload()
        session: UserSession = UserSession()
        _, payload = cls._verify_session(token)
        if not payload.is_default():
            session: UserSession = await cls._retrieve_session(
                user_id=payload.sub, session_id=payload.ssn
            )
            if not session.is_default():
                deleted_session: UserSession = await cls._delete_session(
                    user_id=session.user_id, session_id=session.session_id
                )
                deleted_session.supabase_token = session.supabase_token
                deleted_session.intf_user = session.intf_user
                return deleted_session
            return session
        return session
