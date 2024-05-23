

from .supabase import get_supabase_client
from supabase._async.client import AsyncClient as Client

from supabased.migrations.auth import InsertUserKey
from supabased.queries.auth import FetchUserKey

async def get_insert_user_key(client: Client = None) -> InsertUserKey:
    if client is None:
        client = await get_supabase_client()
    return InsertUserKey(client)

async def get_fetch_user_key(client: Client = None) -> FetchUserKey:
    if client is None:
        client = await get_supabase_client()
    return FetchUserKey(client)