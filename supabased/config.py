# /supabsed/config

import os

# Supabase: connection parameters
SUPABASE_URL: str = os.environ.get("SUPABASE_PROJECT_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_API_KEY")
SUPABASE_SERVICE_ROLE_KEY: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
