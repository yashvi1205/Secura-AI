from __future__ import annotations

from redis import Redis
from rq import Connection, Worker

from backend.app.core.config import settings


def main() -> None:
    conn = Redis.from_url(settings.redis_url)
    with Connection(conn):
        w = Worker([settings.rq_queue])
        w.work()


if __name__ == "__main__":
    main()

