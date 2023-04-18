from fastapi import FastAPI

rating = FastAPI()


@rating.get("/")
async def all_user_ratings():
    return {"message": "All ratings of users"}


@rating.get("/{user_id}")
async def user_rating(user_id: int | None = None):
    return {"message": "User of a single user", "user": user_id}
