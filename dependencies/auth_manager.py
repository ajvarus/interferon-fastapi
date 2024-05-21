# dependencies/auth.py
from fastapi import Depends
from .supabase_auth import get_create_and_login_user, get_login_user, get_logout_user, get_fetch_user


from auth import AuthManager
from supabased.queries.auth import LoginUser, SignoutUser, FetchUser
from supabased.migrations.auth import CreateAndLoginUser

async def get_auth_manager(
    create_and_login_user: CreateAndLoginUser = Depends(get_create_and_login_user),
    login_user: LoginUser = Depends(get_login_user),
    signout_user: SignoutUser = Depends(get_logout_user),
    fetch_user: FetchUser = Depends(get_fetch_user),
) -> AuthManager:
    # Singleton pattern ensures only one instance is created
    instance = AuthManager(
        signup_user=create_and_login_user,
        login_user=login_user,
        signout_user=signout_user,
        fetch_user=fetch_user,
    )
    return instance

from .supabase_auth import test_get_create_and_login_user, test_get_login_user, test_get_logout_user

async def test_get_auth_manager(
    create_and_login_user: CreateAndLoginUser = None,
    login_user: LoginUser = None,
    signout_user: SignoutUser = Depends(),
    fetch_user: FetchUser = Depends(),
) -> AuthManager:
    # Singleton pattern ensures only one instance is created
    create_and_login_user = await test_get_create_and_login_user()
    login_user = await test_get_login_user()
    signout_user = await test_get_logout_user()
    instance = AuthManager(
        signup_user=create_and_login_user,
        login_user=login_user,
        signout_user=signout_user,
        fetch_user=fetch_user,
    )
    return instance
