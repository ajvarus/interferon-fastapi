
from fastapi import Depends
from .supabase import get_supabase_client
from supabase._async.client import AsyncClient as Client

from supabased.migrations.auth import CreateAndLoginUser
from supabased.queries.auth import LoginUser, SignoutUser

async def get_create_and_login_user(client: Client = Depends(get_supabase_client)):
    return CreateAndLoginUser(supabase_client=client)

async def get_login_user(client: Client = Depends(get_supabase_client)):
    return LoginUser(supabase_client=client)

async def test_get_create_and_login_user(client: Client = None):
    client = await get_supabase_client()
    return CreateAndLoginUser(supabase_client=client)

async def test_get_login_user(client: Client = None):
    client = await get_supabase_client()
    return LoginUser(supabase_client=client)

async def get_logout_user(client: Client = Depends(get_supabase_client)):
    return SignoutUser(supabase_client=client)

async def test_get_logout_user(client: Client = None):
    client = await get_supabase_client()
    return SignoutUser(supabase_client=client)