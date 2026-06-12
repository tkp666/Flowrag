from __future__ import annotations

import json
from typing import Any


def make_sse_event(event: str, data: Any) -> str:
    if isinstance(data, str):
        payload = data
    else:
        payload = json.dumps(data, ensure_ascii=False)

    return f"event: {event}\ndata: {payload}\n\n"


def parse_sse_event(chunk: str) -> dict[str, Any]:
    lines = chunk.rstrip("\n").split("\n")
    event = lines[0].removeprefix("event: ")
    raw_data = lines[1].removeprefix("data: ")

    try:
        data: Any = json.loads(raw_data)
    except json.JSONDecodeError:
        data = raw_data

    return {"event": event, "data": data}
