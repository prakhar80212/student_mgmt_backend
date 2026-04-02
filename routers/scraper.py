import asyncio
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from auth_utils import get_current_user

router = APIRouter()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

WORKER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "playwright_worker.py")


class ScrapeRequest(BaseModel):
    url: str


def _run_screenshot(url: str) -> str:
    result = subprocess.run(
        [sys.executable, WORKER, json.dumps(USER_AGENTS), url],
        capture_output=True,
        text=True,
        timeout=90,
    )
    if result.stderr:
        print(result.stderr, flush=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Subprocess failed")
    return result.stdout.strip()


_executor = ThreadPoolExecutor(max_workers=2)


@router.post("/screenshot")
async def screenshot(
    payload: ScrapeRequest,
    _: object = Depends(get_current_user),
):
    try:
        loop = asyncio.get_event_loop()
        image_b64 = await loop.run_in_executor(_executor, _run_screenshot, str(payload.url))
        return {"image": image_b64}
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Screenshot failed: {type(e).__name__}: {str(e)}")
