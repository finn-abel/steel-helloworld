"""Step 2: open a Steel cloud browser and print its live viewer URL. No agent yet."""

import os

from dotenv import load_dotenv
from steel import Steel

load_dotenv()

api_key = os.getenv("STEEL_API_KEY")
if not api_key:
    raise SystemExit("STEEL_API_KEY is missing from .env")

client = Steel(steel_api_key=api_key)

print("Creating Steel session...")
session = client.sessions.create()

print(f"\n  session id   {session.id}")
print(f"  status       {session.status}")
print(f"  watch it at  {session.session_viewer_url}\n")

try:
    input("Press Enter to release the session... ")
except EOFError:
    pass
finally:
    client.sessions.release(session.id)
    print("Session released.")
