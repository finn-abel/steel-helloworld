"""Step 3: attach Browser-Use to a Steel cloud browser over CDP. Still no task."""

import asyncio
import os

from browser_use import Browser
from dotenv import load_dotenv
from steel import Steel

load_dotenv()

api_key = os.getenv("STEEL_API_KEY")
if not api_key:
    raise SystemExit("STEEL_API_KEY is missing from .env")

client = Steel(steel_api_key=api_key)


async def main() -> None:
    print("Creating Steel session...")
    session = client.sessions.create()
    print(f"  watch it at  {session.session_viewer_url}\n")

    browser = Browser(cdp_url=session.websocket_url, is_local=False)
    try:
        print("Attaching Browser-Use over CDP...")
        await browser.start()

        print(f"  cdp connected  {browser.is_cdp_connected}")
        print(f"  open tabs      {len(await browser.get_tabs())}")
        print(f"  current url    {await browser.get_current_page_url()}")
    finally:
        await browser.stop()
        client.sessions.release(session.id)
        print("\nBrowser detached, session released.")


asyncio.run(main())
