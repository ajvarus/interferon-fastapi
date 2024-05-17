from supabased.migrations.auth import CreateAndLoginUser
from supabased.queries.auth import LoginUser, SignoutUser, FetchUser

from supabase._async.client import AsyncClient as Client, create_client

from models.types import SupabaseUser, InterferonUser, SignUpCredentials

from auth import UserSession

from typing import Self



class AuthManager:
    
    _instance: Self = None
    _supabase_client: Client = None

    def __new__(cls, supabase_client: Client) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._supabase_client = supabase_client

            return cls._instance
        return cls._instance
    
    @classmethod
    async def signup(cls, credentials: SignUpCredentials) -> InterferonUser:
        supabase_user: SupabaseUser = await CreateAndLoginUser(cls._supabase_client).sign_up(credentials)

        if supabase_user.user:
            intf_user: InterferonUser = await cls.__sb_to_intf_user_conv(supabase_user)
            return intf_user
        else:
            return InterferonUser()

    @classmethod
    async def login(cls, credentials: SignUpCredentials) -> InterferonUser:
        supabase_user: SupabaseUser = await LoginUser(cls._supabase_client).login_with_password(credentials)

        if supabase_user.user:
            intf_user: InterferonUser = await cls.__sb_to_intf_user_conv(supabase_user)
            return intf_user
        else:
            return InterferonUser()

    @classmethod
    async def logout(cls, jwt: str) -> InterferonUser:
        supabase_user: SupabaseUser = await SignoutUser(cls._supabase_client).sign_out(jwt=jwt)
        if supabase_user is None:
            return InterferonUser()
        else:
            return InterferonUser(is_active=False)

    @classmethod
    async def fetch_current_user(cls):
        pass
        # cls._user = await FetchUser(cls._supabase_client).fetch_user()

    # The below function is used for converting a Supabase user
    # into a Interferon user
    @staticmethod
    async def __sb_to_intf_user_conv(supabase_user: SupabaseUser) -> InterferonUser:
            try:
                return InterferonUser(
                    user_id = supabase_user.user.get("id", None),
                    supabase_token = supabase_user.session.get("access_token", None),
                    token = None,
                    is_active = True,
                    last_active = None
                )
            except Exception as e:
                return InterferonUser() 

