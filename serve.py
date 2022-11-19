"""The DePaul Club Bot."""

import json
import os
import typing as t

from telethon.sync import TelegramClient
from telethon.sync import events

__author__ = "Akshay Mestry (XAMES3) <xa@mes3.dev>"
__version__ = "1.0.1"

# Server credentials
API_ID: t.Final[str] = os.environ["API_ID"]
API_HASH: t.Final[str] = os.environ["API_HASH"]
INPUT_CHANNEL_ID: t.Final[str] = os.environ["INPUT_CHANNEL_ID"]

# Client credentials
BOT_TOKEN: t.Final[str] = os.environ["BOT_TOKEN"]
CHANNEL_ID: t.Final[str] = os.environ["CHANNEL_ID"]

_base_url: str = f"https://discordapp.com/api/channels/{CHANNEL_ID}/messages"
_headers: dict[str, str] = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json",
}


def headers(_headers: dict[str, str] = _headers) -> list[str]:
    """Return list of headers."""
    return [f"-H {f'{key}: {value}'!r}" for key, value in _headers.items()]


def post(message: str) -> None:
    """Post message on client devices."""
    _h = " ".join(headers())
    cmd = ["curl", _h, "-X", "POST", "-d", f"'{message}'", _base_url]
    os.system(f'{" ".join(cmd)}')


with TelegramClient("the-depaul-bot", api_id=API_ID, api_hash=API_HASH) as ctx:

    @ctx.on(events.NewMessage(chats=[int(INPUT_CHANNEL_ID)]))
    async def handler(event: events) -> None:
        _message = event.message.message
        if _message.lower().startswith("no vi"):
            _data = json.dumps({"content": _message})
            print(f"Got: {_message}")
            post(_data)

    init_msg = "Bot initialized..."
    _data = json.dumps({"content": init_msg})
    post(_data)
    ctx.run_until_disconnected()
