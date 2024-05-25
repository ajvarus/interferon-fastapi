
from fastapi import Depends, HTTPException
from supabase._async.client import AsyncClient as Client
from supabase.client import PostgrestAPIResponse as APIResponse

from dependencies.password_encryptor import get_password_encryptor
from dependencies.supabase import get_supabase_client, get_supabase_graphql_client

from features import PasswordEncryptor

from typing import Dict

async def get_graphql_passwords_mutation_context(
    client: Client = Depends(get_supabase_graphql_client),
    encryptor: PasswordEncryptor = Depends(get_password_encryptor)
) -> Dict[str, any]:
    return {"client": client, "encryptor": encryptor}