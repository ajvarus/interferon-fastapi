
from .config import SUPABASE_URL, SUPABASE_KEY
from supabase._async.client import AsyncClient as Client, create_client


class SupabaseManager():

    _client: Client = None

    @classmethod
    async def init(cls):
        if cls._client is None:
            cls._client = await create_client(supabase_url=SUPABASE_URL,
                                          supabase_key=SUPABASE_KEY)
            
    @classmethod
    async def get_client(cls) -> Client:
        if cls._client is None:
            raise Exception("Client not initialised.")
        return cls._client