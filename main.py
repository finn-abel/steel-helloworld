"""Steel + Browser-Use hello world: read the top 5 posts on Hacker News."""

import asyncio
import os

from browser_use import Agent, Browser, ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from steel import Steel
from steel.types import Session

load_dotenv()

TASK = "Go to news.ycombinator.com and return the titles of the top 5 posts, in order."
MODEL = "gpt-4.1-mini"
MAX_STEPS = 10
TOP_N = 5

steel_api_key = os.getenv("STEEL_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
if not steel_api_key or not openai_api_key:
    raise SystemExit("STEEL_API_KEY and OPENAI_API_KEY must both be set in .env")

client = Steel(steel_api_key=steel_api_key)


class TopPosts(BaseModel):
    """The shape we force the agent's answer into."""

    titles: list[str]


async def scrape_top_posts(session: Session) -> TopPosts | None:
    """Attach the agent to the Steel browser, run the task, always detach."""
    browser = Browser(cdp_url=session.websocket_url, is_local=False)
    try:
        agent = Agent(
            task=TASK,
            llm=ChatOpenAI(model=MODEL),
            browser=browser,
            output_model_schema=TopPosts,
        )
        history = await agent.run(max_steps=MAX_STEPS)
        return history.structured_output
    finally:
        # Never let a failed detach stop us from releasing the session below.
        try:
            await browser.stop()
        except Exception as exc:
            print(f"  warning: browser detach failed ({exc})")


def release(session: Session) -> None:
    """Release the Steel session and report what the API says its status is."""
    client.sessions.release(session.id)
    status = client.sessions.retrieve(session.id).status
    print(f"\nSession released (status now: {status})")


def print_posts(result: TopPosts | None) -> None:
    print("\n=== Top 5 on Hacker News ===")
    if result is None:
        print("The agent finished without returning a result.")
        return
    for i, title in enumerate(result.titles[:TOP_N], start=1):
        print(f"{i}. {title}")


async def main() -> None:
    print("Creating Steel session...")
    session = client.sessions.create()
    print(f"\n  watch it at  {session.session_viewer_url}\n")

    # Everything past this point must release the session, however it exits.
    try:
        try:
            input("Open that URL, then press Enter to start the agent... ")
        except EOFError:
            pass
        print_posts(await scrape_top_posts(session))
    finally:
        release(session)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
