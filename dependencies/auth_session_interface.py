
from fastapi import Depends
from .auth_manager import get_auth_manager
from .user_session_engine import get_user_session_engine

from auth import AuthManager, UserSessionEngine, AuthSessionInterface

async def get_auth_session_interface(
        am: AuthManager = Depends(get_auth_manager),
        se: UserSessionEngine = Depends(get_user_session_engine)
) -> AuthSessionInterface:
    return AuthSessionInterface(
        auth_manager=am,
        session_engine=se
    )

from .auth_manager import test_get_auth_manager
from .user_session_engine import test_get_user_session_engine

async def test_get_auth_session_interface(
        am: AuthManager = None,
        se: UserSessionEngine = None
) -> AuthSessionInterface:
    am = await test_get_auth_manager()
    se = await test_get_user_session_engine()
    return AuthSessionInterface(
        auth_manager=am,
        session_engine=se
    )