# src/backend/app/services/caseid.py
import re
from sqlalchemy import select, func
from src.backend.db_files.models import Person
from ..services.db_service import AsyncSessionLocal
import asyncio

PREFIX = "MP2024"

async def generate_next_case_id():
    """
    Generate next MP2024xxxx using the maximum numeric suffix in DB.
    """
    async with AsyncSessionLocal() as session:
        # get max case_id
        stmt = select(func.max(Person.case_id))
        res = await session.execute(stmt)
        max_case = res.scalar_one_or_none()
        if not max_case:
            next_index = 1
        else:
            # parse digits from end
            m = re.search(r"(\d+)$", max_case)
            if m:
                next_index = int(m.group(1)) + 1
            else:
                next_index = 1
        return f"{PREFIX}{next_index:04d}"
