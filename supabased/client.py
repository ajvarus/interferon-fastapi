from .config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
from supabase._async.client import AsyncClient as Client, create_client
from supabase.lib.client_options import ClientOptions


class SupabaseManager:

    _client: Client = None

    @classmethod
    async def init(cls):
        if cls._client is None:
            cls._client = await create_client(
                supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY
            )
        return cls._client

    @classmethod
    async def get_client(cls) -> Client:
        if cls._client is None:
            await cls.init()
        return cls._client

    @classmethod
    async def get_admin_client(cls) -> Client:
        client: Client = await create_client(
            supabase_url=SUPABASE_URL,
            supabase_key=SUPABASE_SERVICE_ROLE_KEY,
        )
        return client

    @classmethod
    async def get_graphql_client(cls) -> Client:
        options = ClientOptions().replace(schema="graphql")
        client: Client = await create_client(
            supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY, options=options
        )
        return client
