import sqlite3
from config import Config

conn = sqlite3.connect(Config.DB_PATH)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS stock (
    product TEXT,
    stock_level INTEGER
)
""")

c.execute("DELETE FROM stock")

products = ["Widget A", "Widget B", "Widget C", "Widget D"]
for p in products:
    c.execute(
        "INSERT INTO stock VALUES (?, ?)",
        (p, 50)
    )

conn.commit()
conn.close()
print("Demo database ready")
