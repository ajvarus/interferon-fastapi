from fastapi import Request, Depends, HTTPException, status

from auth import AuthSessionInterface

from models.types import UserSession

from dependencies.auth_session_interface import get_auth_session_interface

async def get_verified(
    request: Request,
    asi: AuthSessionInterface = Depends(get_auth_session_interface)
) -> None:
    token: str = request.cookies.get('token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token provided"
        )
    session: UserSession = await asi.verify(token)

    if session.is_default():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid"
        )
    elif session.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token"
        )
    else:
        return session
