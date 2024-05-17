

from supabase._async.client import AsyncClient as Client, create_client
from supabased import SupabaseManager

from models.types import SupabaseUser


# This class is responsible for creating and logging in a user by default.
# If successful, returns a User object.
class FetchUser:

    def __init__(self, supabase_client: SupabaseManager) -> None:
        self._sb: Client = supabase_client

    # Supabase: fetch signup response from Users table 
    async def fetch_user(self, jwt: str = None) -> SupabaseUser:
        try:
            user = await self._sb.auth.get_user(jwt)
            print(user)
            return SupabaseUser(user==user.model_dump())
        
        except Exception as e:
            print(str(e))
            return SupabaseUser()
    
