from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

LOCAL_CONFIG_PATH = Path(__file__).parent / "supabase_local.json"


def load_local_config() -> Optional[dict]:
    if not LOCAL_CONFIG_PATH.exists():
        return None
    return json.loads(LOCAL_CONFIG_PATH.read_text())


def is_enabled() -> bool:
    cfg = load_local_config()
    return bool(cfg and cfg.get("url") and cfg.get("publishable_key") and cfg.get("table"))


def insert_reading(payload: dict) -> bool:
    cfg = load_local_config()
    if not cfg:
        return False

    url = cfg["url"].rstrip("/") + f"/rest/v1/{cfg['table']}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "apikey": cfg["publishable_key"],
            "Authorization": f"Bearer {cfg['publishable_key']}",
            "Prefer": "return=minimal",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Supabase insert failed: {e.code} {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Supabase insert failed: {e.reason}") from e
