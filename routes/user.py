from fastapi import APIRouter, Request
from models.users import User
from schema.schema import individual_serial, many_serial
from config.db import users
from bcrypt import gensalt, hashpw,checkpw
from bson import ObjectId
from fastapi import HTTPException, Request, status

userRouter = APIRouter()


# get all users
@userRouter.get("/api/users")
async def get_users():
    try:
        all_users = users.find()
        return many_serial(all_users)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Exception occurred: {e}")
        return {"error": "Internal Server Error"}


@userRouter.post("/api/users/signup")
async def create_user(user: User):
    try:
        user = dict(user)
        exUser =  users.find_one({"email": user["email"]})
        if exUser:
            return {"error": "User already exists"}
        salt = gensalt()
        user["password"] = hashpw(user["password"].encode("utf-8"), salt)
        users.insert_one(user)
        return individual_serial(user)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Exception occurred: {e}")
        return {"error": "Internal Server Error"}

@userRouter.get("/api/users/{id}")
async def get_user(id):
    try:
        user = users.find_one({"_id": ObjectId(id)})
        return individual_serial(user)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Exception occurred: {e}")
        return {"error": "Internal Server Error"}


@userRouter.post("/api/users/login")
async def login_user(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"error": "Email and password are required."}

        exUser = users.find_one({"email": email})

        if not exUser:
            return {"error": "User not found"}

        hashed_password = exUser.get("password", b"")

        if not checkpw(password.encode("utf-8"), hashed_password):
            return {"error": "Invalid credentials"}

        return individual_serial(exUser)

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Exception occurred: {e}")
        return {"error": "Internal Server Error"}
