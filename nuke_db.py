from sqlalchemy import text
from app.db.session import engine

print("Dropping public schema...")
with engine.connect() as conn:
    conn.execute(text("DROP SCHEMA public CASCADE;"))
    conn.execute(text("CREATE SCHEMA public;"))
    conn.commit()

print("Database wiped clean. Ready for fresh migrations.")