from supabase._async.client import AsyncClient as Client

from fastapi import Depends
from dependencies.supabase import get_supabase_client

from models.types import SupabaseUser


class SignoutUser:

    def __init__(self, supabase_client: Client = Depends(get_supabase_client)) -> None:
        self._sb = supabase_client

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
