from fastapi import FastAPI

search = FastAPI()


@search.get("/")
async def search_all():
    return {"message": "Handy dandy search tool maybe?"}


@search.get("/user/{username}")
async def search_user_id(username: str | None = None):
    return {"message": "Returns the id of user with the username", "user": username}
