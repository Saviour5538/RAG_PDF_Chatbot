from backend.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    res = conn.execute(text("SELECT 1"))
    print(res.fetchone())
