
from .auth_manager import AuthManager
from .user_session_engine import UserSessionEngine

from models.types import SignUpCredentials, InterferonUser, UserSession

from typing import Self


class AuthSessionInterface:

    _instance: Self = None
    _am: AuthManager = None
    _se: UserSessionEngine = None

    def __new__(
            cls, 
            auth_manager: AuthManager,
            session_engine: UserSessionEngine
            ) -> Self:
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._am = auth_manager
            cls._se = session_engine
        return cls._instance

    @classmethod
    async def signup_and_start_session(cls, credentials: SignUpCredentials) -> UserSession:
        # Sign up the user with Supabase
        try:
            print(type(cls._am))
            user: InterferonUser = await cls._am.signup(credentials)
            if not user.is_default():
                # Start a session for the new user
                user_session: UserSession = await cls._se.start_session(user)
                if not user_session.is_default():
                    return user_session
        except Exception as e:
            print(str(e))
            pass
        return UserSession()

    @classmethod
    async def login_and_start_session(cls, credentials: SignUpCredentials) -> UserSession:
        # Log in the user with Supabase
        try:
            user: InterferonUser = await cls._am.login(credentials)
            if not user.is_default():
                # Start a session for the authenticated user
                user_session: UserSession = await cls._se.start_session(user)
                if not user_session.is_default():
                    return user_session
                return user_session
        except Exception as e:
            pass
        return UserSession()

    @classmethod
    async def logout_and_terminate_session(cls, token: str) -> UserSession:
        # Log out the user from Supabase
        try:
            # Terminate the user's session
            user_session: UserSession = await cls._se.terminate_session(token)
            if not user_session.is_default():   
                user: InterferonUser = await cls._am.logout(user_session.supabase_token)
                if not user.is_default():
                    return UserSession.from_user(user)
                else: return UserSession()
            else: return UserSession()
        except Exception as e:
            pass
        return UserSession()
    
    @classmethod
    async def verify(cls, token: str) -> bool:
        try:
            session: UserSession = await cls._se.verify_and_retrieve_session(token)
            if not session.is_default():
                if session.is_active:
                    return True
                elif session.is_active == False:
                    await cls._am.logout(session.supabase_token)
                    return False
            else:
                return False
        except Exception as e:
            return False