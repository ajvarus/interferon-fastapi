import os
 # from supabase import create_client, Client
from supabase._async.client import AsyncClient as Client, create_client

# Supabase: connection parameters
url: str = os.environ.get('SUPABASE_PROJECT_URL')
key: str = os.environ.get('SUPABASE_API_KEY')

# Global Supabase client
supabase_client = None

# Supabase: create client
async def init_supabase():
    global supabase_client 
    supabase_client = await create_client(supabase_url=url, 
                                 supabase_key=key)


# Supbase: fetch data from Threads table 
async def fetch_user(id:int):
    global supabase_client
    response = await supabase_client.table('Threads').select('*').eq('user_id', id).execute()
    return response
