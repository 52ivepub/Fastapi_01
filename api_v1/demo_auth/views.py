import secrets
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header, status
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

