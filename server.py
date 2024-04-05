from fastapi import FastAPI
from routes.user import userRouter 
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
app.include_router(userRouter)