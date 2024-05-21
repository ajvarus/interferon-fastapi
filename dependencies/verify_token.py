from fastapi import Request, Depends, HTTPException, status

from auth import AuthSessionInterface

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
    is_valid = await asi.verify(token)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
