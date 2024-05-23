
from supabase._async.client import AsyncClient as SupabaseClient
from supabase.client import PostgrestAPIResponse as APIResponse 


class FetchUserKey:
    def __init__(self, sb: SupabaseClient) -> None:
        self.sb = sb

    async def fetch_user_key(self, uid: str) -> dict:
        row: dict = {}
        try:
            response: APIResponse = await self.sb.table('intf_users').select('master_key').eq('user_id', uid).single().execute()
            if response.data:
                row = response.data
            return row 
        except Exception as e:
            return row