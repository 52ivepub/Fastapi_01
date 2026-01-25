from auth import utils as auth_utils
from ...users.schemas import UserSchema
from fastapi import (
    APIRouter,
)

router = APIRouter(prefix="/jwt", tags=["JWT"])

john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)

sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
)

user_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam, 
}


@router.post("/login/")
def auth_user_issue_jwt(
    user: UserSchema,
):
    pass

