from supabase._async.client import AsyncClient as Client

from gotrue.types import UserResponse
from gotrue.errors import AuthApiError

from typing import Optional


class UserExistenceChecker:

    def __init__(self, supabase_client: Client) -> None:
        self._sb: Client = supabase_client

    async def check_if_user_exists(self, email: str) -> Optional[bool]:
        try:
            response: UserResponse = await self._sb.auth.admin.create_user(
                attributes={"email": email}
            )
            if response.user:
                await self._sb.auth.admin.delete_user(response.user.id)
            return False
        except AuthApiError as e:
            if e.status == 422:
                return True
            return None
        except Exception:
            return None
