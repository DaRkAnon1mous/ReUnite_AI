import asyncio
import ssl
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

ssl_context = ssl.create_default_context()

async def test():
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={"ssl": ssl_context}
    )
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print(result.scalar())

asyncio.run(test())
