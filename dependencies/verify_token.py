from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth import AuthSessionInterface

from models.types import UserSession

from dependencies.auth_session_interface import get_auth_session_interface

bearer_scheme = HTTPBearer()


async def get_verified(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    asi: AuthSessionInterface = Depends(get_auth_session_interface),
) -> None:
    token: str = credentials.credentials
    print(f"Token: {token}")
    # Commenting out to test Authorization header based verification
    # token: str = request.cookies.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token provided"
        )
    session: UserSession = await asi.verify(token)

    if session.is_default():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid")
    elif session.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token"
        )
    else:
        return session
