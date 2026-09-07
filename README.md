# Steel-HelloWorld

Opens Hacker News in a cloud browser and prints the titles of the top 5 posts.

[Steel](https://steel.dev) hosts the Chrome instance and exposes a CDP endpoint plus a live viewer
URL. [Browser-Use](https://browser-use.com) attaches to it and runs the observe–think–act loop:
screenshot the page, ask an OpenAI vision model for the next action, execute it over CDP, repeat.
The final answer is constrained to a Pydantic schema, so you get JSON rather than prose.

A learning project. If you actually want Hacker News titles, use their API.

## Setup

Needs [uv](https://docs.astral.sh/uv/getting-started/installation/), a
[Steel key](https://app.steel.dev/settings/api-keys), and an
[OpenAI key](https://platform.openai.com/api-keys).

```bash
uv sync
cp .env.example .env    # add STEEL_API_KEY and OPENAI_API_KEY
uv run python check_setup.py
```

## Run

```bash
uv run python main.py
```

It prints a viewer URL and waits — open the URL, then press Enter to watch the agent work.
Output is a numbered list of five titles, followed by `Session released`.

## Debugging

Each script tests one layer. Run in order to isolate a failure:

| Script | Checks |
|---|---|
| `check_setup.py` | Packages installed, keys loaded |
| `open_session.py` | Steel accepts the key, returns a live browser |
| `connect_agent.py` | Browser-Use attaches over CDP |

Every session records a replay in the [Steel dashboard](https://app.steel.dev) — usually more
informative than the traceback.

## Notes

Steel bills on session wall-clock time, not activity, so `main.py` releases in a `finally` block —
it survives both an agent crash and Ctrl-C. `MAX_STEPS = 10` overrides Browser-Use's default of
500; each step is a vision call.
