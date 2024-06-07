# /routers/auth/auth.py

from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.enums import AuthType
from models.types import AuthRequest, SignUpCredentials, UserSession

from dependencies.auth_session_interface import get_auth_session_interface
from auth import AuthSessionInterface

from datetime import datetime

from typing import Annotated

router: APIRouter = APIRouter()
bearer_scheme: HTTPBearer = HTTPBearer()


@router.post("/")
async def auth(
    ar: AuthRequest,
    request: Request,
    asi: AuthSessionInterface = Depends(get_auth_session_interface),
) -> UserSession:
    # Handle Signup
    try:
        if ar.auth_type == AuthType.SIGNUP:
            credentials: SignUpCredentials = SignUpCredentials(
                email=ar.email, password=ar.password
            )
            session: UserSession = await asi.signup_and_start_session(credentials)
            if not session.is_default() and session.is_active:
                return session
            elif not session.is_default() and session.is_active == False:
                return session
            return UserSession()

        # Handle Signin
        if ar.auth_type == AuthType.SIGNIN:
            credentials: SignUpCredentials = SignUpCredentials(
                email=ar.email, password=ar.password
            )
            session: UserSession = await asi.login_and_start_session(credentials)
            if not session.is_default() and session.is_active:
                return session
            elif not session.is_default() and session.is_active == False:
                return session
            return UserSession()

        # Handle Signout
        # if ar.auth_type == AuthType.SIGNOUT:
        #     if auth_header := request.headers.get("Authorization"):
        #         if token := (
        #             auth_header.split("Bearer ")[-1]
        #             if "Bearer " in auth_header
        #             else None
        #         ):
        #             session: UserSession = await asi.logout_and_terminate_session(token)
        #             if not session.is_default() and session.is_active == False:
        #                 # Commenting to test Authorization header
        #                 # response.delete_cookie(key="token", path="/")
        #                 return session
        #     return UserSession()

    except Exception as e:
        print(str(e))
        return UserSession()


@router.post("/signout")
async def signout(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    asi: AuthSessionInterface = Depends(get_auth_session_interface),
) -> UserSession:
    token: str = credentials.credentials
    print(token)
    try:
        if token:
            session: UserSession = await asi.logout_and_terminate_session(token)
            if not session.is_default() and session.is_active == False:
                print(session)
                return session
        return UserSession()
    except Exception as e:
        print(str(e))
        return UserSession()
