
from supabase._async.client import AsyncClient as SupabaseClient
from supabase.client import PostgrestAPIResponse as APIResponse 


class InsertUserKey:
    def __init__(self, sb: SupabaseClient) -> None:
        self.sb = sb

    async def insert_user_key(self, uid: str, key: str):
        is_inserted: bool = False
        try:
            data: dict = {
                "user_id": uid,
                "master_key": key
            }
            response: APIResponse = await self.sb.table('intf_users').insert(data).execute()
            if response.data:
                is_inserted = True
            return is_inserted 
        except Exception as e:
            return is_inserted