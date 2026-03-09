from __future__ import annotations

from typing import Any, Optional


def get_queue():  # Returns Optional[Queue]; type omitted to avoid importing rq at load time
    """Lazy Redis/RQ connection so the app starts even when redis is not installed."""
    try:
        from redis import Redis
        from rq import Queue
        from backend.app.core.config import settings
        conn = Redis.from_url(settings.redis_url)
        conn.ping()
        return Queue(settings.rq_queue, connection=conn)
    except Exception:
        return None


def try_enqueue(func: Any, *args: Any, **kwargs: Any) -> bool:
    q = get_queue()
    if not q:
        return False
    q.enqueue(func, *args, **kwargs)
    return True

