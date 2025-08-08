from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

def get_Supabase():    
    url: str = os.environ.get("VITE_SUPABASE_URL")
    key: str = os.environ.get("VITE_SUPABASE_ANON_KEY")
    supabase: Client = create_client(url, key)
    return supabase

if __name__ == "__main__":
    get_Supabase()
