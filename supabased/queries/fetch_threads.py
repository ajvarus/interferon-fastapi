
from supabased import SupabaseManager


class FetchThreads:

    def __init__(self) -> None:
        self.sb = None
        
    async def initialize(self):
        self.sb = await SupabaseManager.get_client()

    # Supbase: fetch data from Threads table 
    async def fetch_threads(self, id:int):
        if self.sb is None:
            await self.initialize()
        threads = await self.sb.table('Threads').select('*').eq('user_id', id).execute()
        return threads