from fastapi import HTTPException, status, Cookie
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from pydantic import BaseModel
from ..models import User, mudemy_session
from ..services import UserService
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
SECRET_KEY = "Please dont look at my secret key, if you take this key then u can stole all my data..."
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

user_service = UserService(mudemy_session)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class CurrentUser(BaseModel):
    user_id: str
    role: str 

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user_from_session(
    # session_id: str | None = Cookie(None, alias="session_id") 
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        role_str: str = payload.get("role")
        print("Decoded payload:", payload)
        if user_id is None or role_str is None:
            raise credentials_exception
        return CurrentUser(user_id=user_id, role=role_str)
    except JWTError:
        raise credentials_exception

# def get_current_user_from_session(
#     session_id: str | None = Cookie(None, alias="session_id") 
#     # token: str = Depends(oauth2_scheme)
# ):
#     print("session id", session_id)
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Cookie"},
#     )

#     if session_id is None:
#         raise credentials_exception

#     try:
#         #Verify Signature
#         print("Decoding session_id:", session_id)
#         payload = jwt.decode(session_id, SECRET_KEY, algorithms=[ALGORITHM])
        
#         user_id: int = payload.get("sub")
#         role_str: str = payload.get("role")
#         print("Decoded payload:", payload)
#         if user_id is None or role_str is None:
#             raise credentials_exception
        
#         return CurrentUser(user_id=user_id, role=role_str)

#     except JWTError:
#         raise credentials_exception