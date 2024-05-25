
from supabase._async.client import AsyncClient as Client, create_client
from supabased import SupabaseManager

async def get_supabase_client() -> Client:
    return await SupabaseManager.get_client()

async def get_supabase_graphql_client() -> Client:
    return await SupabaseManager.get_graphql_client()
