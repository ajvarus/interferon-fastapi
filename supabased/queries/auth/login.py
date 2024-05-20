
from supabase._async.client import AsyncClient as Client, create_client

from fastapi import Depends
from dependencies.supabase import get_supabase_client

from models.types import SignUpCredentials
from models.types import SupabaseUser

# This class is responsible for creating and logging in a user by default.
# If successful, returns a User object.
class LoginUser:

    def __init__(self, supabase_client: Client = Depends(get_supabase_client)) -> None:
        self._sb = supabase_client

    # Supabase: fetch signup response from Users table 
    async def login_with_password(self, credentials: SignUpCredentials) -> SupabaseUser:
        try:
            login_response = await self._sb.auth.sign_in_with_password(credentials=credentials.model_dump())
            supabase_user = SupabaseUser(
                                user=login_response.user.model_dump(),
                                session=login_response.session.model_dump()
                            )
            return supabase_user
        except Exception as e:
            print(str(e))
            return SupabaseUser()
    

# Test template for async function: Remove before commiting to production
# import asyncio
# async def test_login():
#     supabase_client = await SupabaseManager.init()
#     credentials = SignUpCredentials(email="shelter8@ymail.com",
#                                     password="reset123")
#     signup_response = await LoginUser(supabase_client).login_with_password(credentials=credentials)
#     print(signup_response.user.get("id"), signup_response.session.get("access_token", None))

# asyncio.run(test_login())