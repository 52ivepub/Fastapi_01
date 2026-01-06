import asyncio
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="john")
        # await create_user(session=session, username="sam")
        user_sam = await get_user_by_username(session=session, username="sam")
        user_john = await get_user_by_username(session=session, username="john")
        # user_bob = await get_user_by_username(session=session, username="bob")
        await create_user_profile(
            session=session,
            user_id=user_john.id,
            first_name="john",
        )
        await create_user_profile(
            session=session,
            user_id=user_sam.id,
            first_name="sam",
            last_name="White"
        )
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
