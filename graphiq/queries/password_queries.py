# /graphiq/mutations/password_mutations.py

from fastapi import HTTPException
from supabase._async.client import AsyncClient as Client
from supabase.client import PostgrestAPIResponse as APIResponse

import strawberry

from graphiq.types import PasswordFetchResponse

from features import PasswordEncryptor

from typing import List, Dict


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
                    decrypted_passwords: List[PasswordFetchResponse] = (
                        await encryptor.decrypt_passwords(passwords=fetched_passwords)
                    )

                    return decrypted_passwords
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to insert passwords into the database.",
                )
        except Exception as e:
            return HTTPException(status_code=401, detail=f"Save failed: {str(e)}")
