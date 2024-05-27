# /graphiq/mutations/password_mutations.py

from fastapi import HTTPException
from supabase._async.client import AsyncClient as Client
from supabase.client import PostgrestAPIResponse as APIResponse

import strawberry

from graphiq.types import PasswordInput, PasswordRequest, PasswordResponse

from features import PasswordEncryptor

from typing import List

from models.enums import OpType


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def store_passwords(
        self, passwords: List[PasswordInput], info: strawberry.Info
    ) -> List[PasswordResponse]:
        context: dict = info.context
        client: Client = context.get("client")
        encryptor: PasswordEncryptor = context.get("encryptor")
        if not passwords:
            raise HTTPException(
                status_code=400, detail="The list of passwords is empty."
            )
        try:
            query = """#graphql
                mutation($objects: [passwordsInsertInput!]!) {
                insertIntopasswordsCollection(objects: $objects) {
                        records {
                            id
                            password_name
                            encrypted_password
                        }
                    }
                }
            """
            encrypted_passwords: List[PasswordRequest] = (
                await encryptor.encrypt_passwords(passwords=passwords)
            )
            variables = {
                "objects": [
                    {
                        "user_id": ep.user_id,
                        "password_name": ep.password_name,
                        "encrypted_password": ep.encrypted_password,
                    }
                    for ep in encrypted_passwords
                ]
            }

            response: APIResponse = await client.rpc(
                "resolve", {"query": query, "variables": variables}
            ).execute()

            if response.data:
                if (
                    inserted_passwords := response.data.get("data")
                    .get("insertIntopasswordsCollection")
                    .get("records")
                ):
                    if is_added_to_cache := await encryptor.cache_passwords(
                        inserted_passwords, OpType.ADD
                    ):
                        return [
                            PasswordResponse(
                                id=p.get("id"),
                                password_name=p.get("password_name"),
                                encrypted_password=p.get("encrypted_password"),
                            )
                            for p in inserted_passwords
                        ]
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to insert passwords into the database.",
                )
        except Exception as e:
            return HTTPException(status_code=401, detail=f"Save failed: {str(e)}")
