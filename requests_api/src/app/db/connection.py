from contextlib import asynccontextmanager
from aiochclient import ChClient
from aiohttp import ClientSession
from app.config import settings
from app.utils.logger import logger

@asynccontextmanager
async def clickhouse_client():
    session = ClientSession()
    client = ChClient(
        session,
        url=f"http://{settings.CLICKHOUSE_HOST}:8123",
        user=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
        database=settings.CLICKHOUSE_DB
    )
    try:
        await client.execute(f"""
            CREATE TABLE IF NOT EXISTS {settings.CLICKHOUSE_DB}.requests (
                id UUID DEFAULT generateUUIDv4(),
                user_id Int32,
                title String,
                description String,
                status String DEFAULT 'pending',
                created_at DateTime DEFAULT now(),
                updated_at DateTime DEFAULT now()
            ) ENGINE = MergeTree()
            ORDER BY (created_at, status)
        """)
        yield client
    finally:
        await session.close()