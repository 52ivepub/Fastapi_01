import secrets
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
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


def get_auth_user_username(
        credentilals: Annotated[HTTPBasicCredentials, Depends(security)],
):
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

