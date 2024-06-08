from supabase._async.client import AsyncClient as Client
from supabased import SupabaseManager


async def get_supabase_client() -> Client:
    return await SupabaseManager.get_client()


async def get_supabase_admin_client() -> Client:
    return await SupabaseManager.get_admin_client()


async def get_supabase_graphql_client() -> Client:
    return await SupabaseManager.get_graphql_client()
