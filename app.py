from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from graphql_server import graphql_app
from supabase_client import init_supabase

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_event_handler("startup", init_supabase)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def home():
    return {
        "message": "graphql"
    }