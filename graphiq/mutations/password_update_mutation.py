# /graphic/mutations/password_update_mutation.py

from fastapi import HTTPException

from supabase._async.client import AsyncClient as Client
from supabase.client import PostgrestAPIResponse as APIResponse

from redis import RedisError

import strawberry

from graphiq.types import PasswordUpdateInput, PasswordResponse

from features import PasswordEncryptor

from models.enums import OpType

from typing import List, Dict


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def update_passwords(
        self,
        passwords: List[PasswordUpdateInput],
        info: strawberry.Info,
    ) -> List[PasswordResponse]:
        context: dict = info.context
        user_id: str = context.get("user_id")
        client: Client = context.get("client")
        encryptor: PasswordEncryptor = context.get("encryptor")

        updated_passwords: List[PasswordResponse] = []

        for p in passwords:
            encrypted_password = await encryptor.encrypt_single_password(p.password)
            set_object = {
                "password_name": p.password_name,
                "encrypted_password": encrypted_password,
            }
            filter_object = {"id": {"eq": int(p.id)}, "user_id": {"eq": user_id}}
            query = """#graphql
                mutation($set: passwordsUpdateInput!, $filter: passwordsFilter!) {
                    updatepasswordsCollection(
                        set: $set,
                        filter: $filter
                    ) {
                        records {
                            id
                            password_name
                            encrypted_password
                        }
                    }
                }
            """
            variables = {"set": set_object, "filter": filter_object}

            try:
                response: APIResponse = await client.rpc(
                    "resolve", {"query": query, "variables": variables}
                ).execute()

                if response.data:
                    if (
                        updated_records := response.data.get("data")
                        .get("updatepasswordsCollection")
                        .get("records")
                    ):
                        updated_passwords.extend(
                            [
                                PasswordResponse(
                                    id=record.get("id"),
                                    password_name=record.get("password_name"),
                                    encrypted_password=record.get("encrypted_password"),
                                )
                                for record in updated_records
                            ]
                        )
                else:
                    raise HTTPException(
                        status_code=400, detail="Failed to update passwords."
                    )
            except Exception as e:
                raise HTTPException(status_code=401, detail=f"Update failed: {str(e)}")

        updated_passwords_to_cache: List[Dict] = [
            password_reponse.to_dict() for password_reponse in updated_passwords
        ]
        try:
            is_updated_in_cache: bool = await encryptor.cache_passwords(
                updated_passwords_to_cache, OpType.UPDATE
            )
            return updated_passwords if is_updated_in_cache else RedisError
        except RedisError as e:
            raise HTTPException(status_code=401, detail=f"Update failed: {str(e)}")
