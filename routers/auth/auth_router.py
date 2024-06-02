# /routers/auth/auth.py

from fastapi import APIRouter, Request, Response, Cookie, Depends

from models.enums import AuthType
from models.types import AuthRequest, SignUpCredentials, UserSession

from dependencies.auth_session_interface import get_auth_session_interface
from auth import AuthSessionInterface

from datetime import datetime

router: APIRouter = APIRouter()


@router.post("/")
async def auth(
    ar: AuthRequest,
    request: Request,
    response: Response,
    asi: AuthSessionInterface = Depends(get_auth_session_interface),
    token=Cookie(None),
) -> UserSession:
    # Handle Signup
    try:
        if ar.auth_type == AuthType.SIGNUP:
            credentials: SignUpCredentials = SignUpCredentials(
                email=ar.email, password=ar.password
            )
            session: UserSession = await asi.signup_and_start_session(credentials)
            if not session.is_default() and session.is_active:
                response.set_cookie(
                    key="token",
                    value=session.token,
                    httponly=True,
                    samesite="none",
                    secure=False,
                    # secure=request.url.scheme == "https",
                    max_age=int(float(session.expiry) - datetime.now().timestamp()),
                    path="/",
                )
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
                response.set_cookie(
                    key="token",
                    value=session.token,
                    httponly=True,
                    samesite="none",
                    secure=False,
                    # secure=request.url.scheme == "https",
                    max_age=int(float(session.expiry) - datetime.now().timestamp()),
                    path="/",
                )
                return session
            elif not session.is_default() and session.is_active == False:
                return session
            return UserSession()

        # Handle Signout
        if ar.auth_type == AuthType.SIGNOUT:
            if token is not None:
                session: UserSession = await asi.logout_and_terminate_session(token)
                if not session.is_default() and session.is_active == False:
                    response.delete_cookie(key="token", path="/")
                    return session
            return UserSession()

    except Exception as e:
        print(str(e))
        return UserSession()
