"""Confirm the environment is ready before we write any agent code."""

import os
from importlib.metadata import version

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, Browser, ChatOpenAI  # noqa: F401
from steel import Steel  # noqa: F401

print(f"browser-use   {version('browser-use')}")
print(f"steel-sdk     {version('steel-sdk')}")

for name in ("STEEL_API_KEY", "OPENAI_API_KEY"):
    value = os.getenv(name)
    if not value or value.startswith("your-"):
        print(f"{name:<18} MISSING (still a placeholder)")
    else:
        print(f"{name:<18} loaded ({value[:6]}...{value[-4:]})")
