import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config.db_config import get_db_connection

with open('app/sql/create_tables.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

try:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Database updated successfully.")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn:
        conn.close()
