from sqlalchemy import inspect
from app.db.session import engine

inspector = inspect(engine)

tables = inspector.get_table_names()
print("Tables in database:", tables)
print("-" * 40)

for table in tables:
    print(f"Table: {table}")
    columns = inspector.get_columns(table)
    for col in columns:
        print(f"  - {col['name']} : {col['type']}")
    print("-" * 40)