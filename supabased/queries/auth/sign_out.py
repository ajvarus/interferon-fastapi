
from supabase._async.client import AsyncClient as Client, create_client

from models.types import SupabaseUser

# This class is responsible for creating and logging in a user by default.
# If successful, returns a User object.
class SignoutUser:

    def __init__(self, supabase_client: Client) -> None:
        self._sb = supabase_client

    # Supabase: fetch signup response from Users table 
    async def sign_out(self, jwt: str) -> SupabaseUser | None:
        
        try:
            signout_response = await self._sb.auth.admin.sign_out(jwt=jwt)
            if signout_response is None:
                return SupabaseUser()
            else:
                raise Exception("Log out unsuccessful.")
            
        except Exception as e:
            print(str(e))
            return None
    

# Test template for async function: Remove before commiting to production
# import asyncio
# async def test_login():
#     supabase_client = await SupabaseManager.init()
#     signup_response = await SignoutUser(supabase_client).sign_out()
#     print(signup_response.user.get("id"), signup_response.session.get("access_token", None))

# asyncio.run(test_login())