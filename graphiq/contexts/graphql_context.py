
from fastapi import Depends, Security
from supabase._async.client import AsyncClient as Client

from dependencies.password_encryptor import get_password_encryptor
from dependencies.supabase import get_supabase_graphql_client
from dependencies.verify_token import get_verified

from models.types import UserSession

from features import PasswordEncryptor

from typing import Dict

async def get_graphql_context(
    session: UserSession = Security(get_verified),
    client: Client = Depends(get_supabase_graphql_client),
    encryptor: PasswordEncryptor = Depends(get_password_encryptor)
) -> Dict[str, any]:
    return {
        "user_id": session.user_id,
        "client": client, 
        "encryptor": encryptor
    }