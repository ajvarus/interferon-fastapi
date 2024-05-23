
from supabased.migrations.auth import CreateAndLoginUser
from supabased.queries.auth import LoginUser, SignoutUser, FetchUser

from models.types import SupabaseUser, InterferonUser, SignUpCredentials

from typing import Self


class AuthManager:
    
    _instance: Self = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            return cls._instance
        return cls._instance
    
    def __init__(
            self, 
            signup_user: CreateAndLoginUser,
            login_user: LoginUser,
            signout_user: SignoutUser,
            fetch_user: FetchUser
                 ) -> None:
        if not hasattr(self, '_initialised'):
            self.signup_user = signup_user
            self.login_user = login_user
            self.signout_user = signout_user
            self.fetch_user = fetch_user
            self._initialised = True

    
    async def signup(self, credentials: SignUpCredentials) -> InterferonUser:
        supabase_user: SupabaseUser = await self.signup_user.sign_up(credentials)
        if not supabase_user.is_default():
            intf_user: InterferonUser = AuthManager.__sb_to_intf_user_conv(supabase_user)
            intf_user.is_new = True
            return intf_user
        else:
            return InterferonUser()

    async def login(self, credentials: SignUpCredentials) -> InterferonUser:
        supabase_user: SupabaseUser = await self.login_user.login_with_password(credentials)
        if not supabase_user.is_default():
            intf_user: InterferonUser = AuthManager.__sb_to_intf_user_conv(supabase_user)
            intf_user.is_new = False
            return intf_user
        else:
            return InterferonUser()

    async def logout(self, jwt: str) -> InterferonUser:
        supabase_user: SupabaseUser = await self.signout_user.sign_out(jwt=jwt)
        if supabase_user is None:
            return InterferonUser()
        else:
            return InterferonUser(is_active=False, is_new=False)

    async def fetch_current_user(self):
        pass
        # cls._user = await FetchUser(cls._supabase_client).fetch_user()

    # The below function is used for converting a Supabase user
    # into a Interferon user
    @staticmethod
    def __sb_to_intf_user_conv(supabase_user: SupabaseUser) -> InterferonUser:
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


