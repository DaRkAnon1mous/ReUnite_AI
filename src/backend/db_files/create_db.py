import asyncio
from backend.db_files.database import init_db

async def main():
    await init_db()
    print("Database tables created.")

if __name__ == "__main__":# - Ensures this script runs only when executed directly 
    asyncio.run(main()) # - Uses asyncio.run() to execute the asynchronous main() function.


