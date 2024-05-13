from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from graphiq import graphql_app

from supabased import SupabaseManager

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_event_handler("startup", SupabaseManager.init)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def home():
    return {
        "message": "graphql"
    }