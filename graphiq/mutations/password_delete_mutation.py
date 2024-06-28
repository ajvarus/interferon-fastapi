# /graphiq/mutations/password_delete_mutation.py

import strawberry

from fastapi import HTTPException

from supabase._async.client import AsyncClient as Client
from supabase.client import PostgrestAPIResponse as APIResponse

from features import PasswordEncryptor

from graphiq.types import PasswordDeleteInput, PasswordResponse

from models.enums import OpType

from typing import List


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def delete_passwords(
        self, passwords: List[PasswordDeleteInput], info: strawberry.Info
    ) -> List[PasswordResponse]:
        context: dict = info.context
        user_id: str = context.get("user_id")
        client: Client = context.get("client")
        encryptor: PasswordEncryptor = context.get("encryptor")

        if not passwords:
            raise HTTPException(
                status_code=400, detail="The list of password IDs is empty."
            )

        ids: List[str] = [int(p.id) for p in passwords]

        try:
            query = """#graphql
                mutation ($user_id: UUID!, $ids: [Int!]!, $atMost: Int!) {
                    deleteFrompasswordsCollection(
                        filter: {user_id: {eq: $user_id}, id: {in: $ids},},
                        atMost: $atMost
                    ) {
                        records {
                        id
                        password_name
                        }
                    }
                }
            """
            variables = {
                "user_id": user_id,
                "ids": ids,
                "atMost": len(ids),
            }

            response: APIResponse = await client.rpc(
                "resolve", {"query": query, "variables": variables}
            ).execute()

            if response.data:
                deleted_passwords = (
                    response.data.get("data")
                    .get("deleteFrompasswordsCollection")
                    .get("records")
                )
                is_deleted: bool = await encryptor.cache_passwords(
                    deleted_passwords, op_type=OpType.DELETE
                )
                if is_deleted:
                    return [
                        PasswordResponse(
                            id=p.get("id"),
                            password_name=p.get("password_name"),
                            username="",
                            encrypted_password="",
                        )
                        for p in deleted_passwords
                    ]
                else:
                    raise HTTPException(
                        status_code=401, detail=f"Failed to delete passwords in cache."
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to delete passwords from the database.",
                )
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Delete failed: {str(e)}")
