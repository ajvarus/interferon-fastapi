from .auth_manager import AuthManager
from .user_session_engine import UserSessionEngine
from cypher.key import manageuserkey

from dependencies.key_manager import get_key_manager

from models.types import SignUpCredentials, InterferonUser, UserSession

from errors.types import SessionError

from typing import Self


class AuthSessionInterface:

    _instance: Self = None
    _am: AuthManager = None
    _se: UserSessionEngine = None

    def __new__(
        cls, auth_manager: AuthManager, session_engine: UserSessionEngine
    ) -> Self:
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._am = auth_manager
            cls._se = session_engine
        return cls._instance

    @classmethod
    @manageuserkey(get_key_manager)
    async def resolve_and_start_session(
        cls, credentials: SignUpCredentials
    ) -> UserSession:
        try:
            user: InterferonUser = await cls._am.resolve(credentials)
            if not user.is_default():
                try:
                    user_session: UserSession = await cls._se.start_session(user)
                    if not user_session.is_default():
                        return user_session
                except SessionError as e:
                    return UserSession(user_id=user.user_id, error_info=e.to_dict())
        except Exception:
            pass
        return UserSession()

    @classmethod
    @manageuserkey(get_key_manager)
    async def signup_and_start_session(
        cls, credentials: SignUpCredentials
    ) -> UserSession:
        try:
            user: InterferonUser = await cls._am.signup(credentials)
            if not user.is_default():
                user_session: UserSession = await cls._se.start_session(user)
                if not user_session.is_default():
                    return user_session
        except Exception as e:
            print(str(e))
        return UserSession()

    @classmethod
    @manageuserkey(get_key_manager)
    async def login_and_start_session(
        cls, credentials: SignUpCredentials
    ) -> UserSession:
        try:
            user: InterferonUser = await cls._am.login(credentials)
            if not user.is_default():
                user_session: UserSession = await cls._se.start_session(user)
                if not user_session.is_default():
                    return user_session
                return user_session
        except Exception as e:
            pass
        return UserSession()

    @classmethod
    @manageuserkey(get_key_manager)
    async def logout_and_terminate_session(cls, token: str) -> UserSession:
        try:
            user_session: UserSession = await cls._se.terminate_session(token)
            if not user_session.is_default():
                logged_out_user: InterferonUser = await cls._am.logout(
                    user_session.supabase_token
                )
                if not logged_out_user.is_default():
                    user_session.intf_user.transfer_non_none_values_from(
                        logged_out_user
                    )
                    user = user_session.intf_user
                    return UserSession.from_user(user)
                else:
                    return UserSession()
            else:
                return UserSession()
        except Exception as e:
            pass
        return UserSession()

    @classmethod
    async def verify(cls, token: str) -> bool:
        try:
            session: UserSession = await cls._se.verify_and_retrieve_session(token)
            if not session.is_default():
                if session.is_active:
                    return session
                elif session.is_active == False:
                    await cls._am.logout(session.supabase_token)
                    return session
            else:
                return session
        except Exception as e:
            return UserSession()

    @classmethod
    async def force_logout_and_terminate_all_sessions(cls, user_id: str) -> bool:
        return await cls._se.force_terminate_all_sessions(user_id)
