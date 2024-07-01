from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from graphiq import graphql_app

from routers.services import password_vault_router

from routers.auth import auth_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8080",
    "https://interferon-live.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")
app.include_router(password_vault_router, prefix="/services")
app.include_router(auth_router, prefix="/auth")


@app.get("/")
async def home():
    return {"message": "graphql"}
