# /supabase/queries/auth/fetch_user.py

from supabase._async.client import AsyncClient as Client
from gotrue.errors import AuthApiError

from models.types import SignUpCredentials
from models.types import SupabaseUser
from models.types.supabase_user import Existed

from typing import Tuple


class FetchUser:

    def __init__(self, supabase_client: Client) -> None:
        self._sb: Client = supabase_client

    async def fetch_user(
        self, credentials: SignUpCredentials
    ) -> Tuple[SupabaseUser, Existed]:
        existed: Existed = False
        try:
            signup_response = await self._sb.auth.sign_up(
                credentials=credentials.model_dump()
            )
            return (
                SupabaseUser(
                    user=signup_response.user.model_dump(),
                    session=signup_response.session.model_dump(),
                ),
                existed,
            )
        except AuthApiError as e:
            if e.status == 422:
                existed = True
                return SupabaseUser(), existed
            return SupabaseUser()
        except Exception as e:
            return SupabaseUser(), None
