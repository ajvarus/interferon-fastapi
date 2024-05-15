
from supabased import SupabaseManager

from fastapi import HTTPException

from models.types import SignUpCredentials
from models.types import SupabaseUser

# This class is responsible for creating and logging in a user by default.
# If successful, returns a User object.
class CreateAndLoginUser:

    def __init__(self, supabase_client: SupabaseManager) -> None:
        self.sb = supabase_client

    # Supabase: fetch signup response from Users table 
    async def sign_up(self, credentials: SignUpCredentials) -> SupabaseUser:
        
        try:
            signup_response = await self.sb.auth.sign_up(credentials=credentials.model_dump())
            supabase_user = SupabaseUser(user=signup_response.user.dict(),
                         session=signup_response.session.dict())
            return supabase_user
        
        except Exception as e:
            return SupabaseUser(user=None,
                                session=None)
    

# Test template for async function: Remove before commiting to production
# import asyncio
# async def test_sign_up():
#     supabase_client = await SupabaseManager.init()
#     credentials = SignUpCredentials(email="shelter7@ymail.com",
#                                     password="reset123")
#     signup_response = await CreateAndLoginUser(supabase_client).sign_up(credentials=credentials)
#     print(signup_response.user.get("id"), signup_response.session.get("access_token"))

# asyncio.run(test_sign_up())