from database import Base, engine
from models import *
from sqlalchemy.exc import OperationalError

print("Creating all tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
except OperationalError as e:
    print("Failed to connect to the database:")
    print(str(e).strip())
    print()
    print("Possible causes and remediation:")
    print("- Wrong DATABASE_URL or wrong password for the DB user.")
    print("  * Set DATABASE_URL environment variable, e.g.:")
    print("    (PowerShell)  $env:DATABASE_URL = 'postgresql+psycopg2://user:password@host:5432/dbname'")
    print("    (bash)        export DATABASE_URL='postgresql+psycopg2://user:password@host:5432/dbname'")
    print("- PostgreSQL server is not running or not reachable on host/port.")
    print("  * Start PostgreSQL service or verify host/port.")
    print("- Authentication method in pg_hba.conf may require different credentials (peer/ident).")
    print("  * Ensure the user exists and uses password authentication (md5/peer settings).")
    print("- To manually verify connection, try:")
    print("    psql -h localhost -U postgres -W")
    print()
    print("After fixing credentials or DB server, re-run create_tables.py")
    raise
