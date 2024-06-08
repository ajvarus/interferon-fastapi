from supabase._async.client import AsyncClient as Client

from models.types import SignUpCredentials
from models.types import SupabaseUser


# This class is responsible for creating and logging in a user by default.
# If successful, returns a User object.
class CreateAndLoginUser:

    def __init__(self, supabase_client: Client) -> None:
        self._sb = supabase_client

    # Supabase: fetch signup response from Users table
    async def sign_up(self, credentials: SignUpCredentials) -> SupabaseUser:
        try:
            signup_response = await self._sb.auth.sign_up(
                credentials=credentials.model_dump()
            )
            return SupabaseUser(
                user=signup_response.user.model_dump(),
                session=signup_response.session.model_dump(),
            )
        except Exception as e:
            print(str(e))
            return SupabaseUser()


# Test template for async function: Remove before commiting to production
# import asyncio
# async def test_sign_up():
#     supabase_client = await SupabaseManager.init()
#     credentials = SignUpCredentials(email="shelter14@ymail.com",
#                                     password="reset123")

#     signup_response = await CreateAndLoginUser(supabase_client).sign_up(credentials=credentials)
#     print(signup_response.user.get("id"), signup_response.session.get("access_token"))

# asyncio.run(test_sign_up())
