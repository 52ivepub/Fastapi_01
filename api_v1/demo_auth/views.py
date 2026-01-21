import secrets
import time
from typing import Annotated, Any
import uuid
from fastapi import APIRouter, Cookie, Depends, HTTPException, Header, Response, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from requests import status_codes

router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()


@router.get("/basic-auth/")
def demo_basic_auth_credentilals(
    credentilals: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hi==))",
        "username": credentilals.username,
        "password": credentilals.password,
    }

usernames_to_passwords = {
    "admin": "admin",
    "john": "password",

}

static_auth_token_to_username = {
    "764dbc6da94ceaf7281b6dd61c0f465a": "admin",
    "2f46e9f2ae7a6f81bb690087d67e65d1": "john",

}


def get_username_by_static_auth_token(
        static_token: str = Header(alias="x-auth-token")
): 
    if username :=  static_auth_token_to_username.get(static_token):
        return username    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid"
    )
    



def get_auth_user_username(
        credentilals: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
    headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_passwords.get(credentilals.username)
    if correct_password is None:
        raise unauthed_exc
    # secrets
    if not secrets.compare_digest(
        credentilals.password.encode("utf-8"),
        correct_password.encode("utf-8"),

    ):
        raise unauthed_exc
    
    return credentilals.username



@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username), 
):
    return {
        "message": f"Hi==))  {auth_username}",
        "username": auth_username,
        
    }


@router.get("/some-http-header-auth/")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token), 
):
    return {
        "message": f"Hi==))  {username}",
        "username": username,
        
    }

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"

def generate_session_id():
    return uuid.uuid4().hex


def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated"
        )
    return COOKIES[session_id]


@router.post("/login-cookie/")
def demo_auth_login_cookie(
    response: Response,
    # auth_username: str = Depends(get_auth_user_username), 
    username: str = Depends(get_username_by_static_auth_token), 
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": username,
        "login_at": int(time.time())
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "ok"}
    

@router.get("/check-cookie")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"Hello {username}",
        **user_session_data
    }


@router.get("/logout-cookie")
def demo_logout_check_cookie(
    respone: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id,)
    respone.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"Bye {username}",
        
    }

