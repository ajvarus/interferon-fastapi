# /graphiq/mutations/password_mutations.py

from fastapi import HTTPException, status
from supabase._async.client import AsyncClient as Client
from supabase.client import PostgrestAPIResponse as APIResponse

import strawberry

from graphiq.types import PasswordFetchResponse, PasswordCacheResponse

from features import PasswordEncryptor

from typing import List, Dict

from models.enums import OpType


@strawberry.type
class Query:
    @strawberry.field
    async def get_passwords(self, info: strawberry.Info) -> List[PasswordFetchResponse]:
        context: dict = info.context
        user_id: str = context.get("user_id")
        client: Client = context.get("client")
        encryptor: PasswordEncryptor = context.get("encryptor")
        try:
            query = """#graphql
                query ($user_id: UUID!) {
                    passwordsCollection(filter: {user_id: {eq: $user_id}}) {
                        edges {
                            node {
                                id
                                password_name
                                username
                                encrypted_password
                            }
                        }
                    }
                }
            """
            variables = {"user_id": user_id}

            response: APIResponse = await client.rpc(
                "resolve", {"query": query, "variables": variables}
            ).execute()

            if response.data:
                if (
                    fetched_passwords := response.data.get("data")
                    .get("passwordsCollection")
                    .get("edges")
                ):
                    fetched_passwords = [node.get("node") for node in fetched_passwords]
                    if is_written_to_cache := await encryptor.cache_passwords(
                        fetched_passwords, OpType.WRITE
                    ):
                        decrypted_passwords: List[PasswordFetchResponse] = (
                            await encryptor.decrypt_passwords(
                                passwords=fetched_passwords
                            )
                        )
                    return decrypted_passwords
                else:
                    return []
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to retrieve passwords from database.",
                )
        except Exception as e:
            return HTTPException(status_code=401, detail=f"Application error: {str(e)}")

    @strawberry.field
    async def get_passwords_from_cache(
        self, password_ids: List[str], info: strawberry.Info
    ) -> List[PasswordCacheResponse]:
        context: dict = info.context
        encryptor: PasswordEncryptor = context.get("encryptor")
        decrypted_passwords: List[dict] = await encryptor.retrieve_passwords_from_cache(
            password_ids
        )
        if decrypted_passwords:
            return decrypted_passwords
        else:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, detail="Cache corrupted!!"
            )
