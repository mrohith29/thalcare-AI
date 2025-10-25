from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

def get_Supabase() -> Client:
    """Create a Supabase client for backend usage.

    Prefer the service role key to perform server-side operations that interact with
    RLS-protected tables (e.g., inserting into `profiles`, `patients`, etc.).
    Falls back to anon key if service key is not provided.
    """
    url: str = os.environ.get("VITE_SUPABASE_URL")
    service_key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    anon_key: str = os.environ.get("VITE_SUPABASE_ANON_KEY")

    if not url:
        raise RuntimeError("Missing SUPABASE_URL environment variable")

    key_to_use = service_key or anon_key
    if not key_to_use:
        raise RuntimeError("Missing SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY environment variable")

    supabase: Client = create_client(url, key_to_use)
    return supabase

if __name__ == "__main__":
    get_Supabase()
