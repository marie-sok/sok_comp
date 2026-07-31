import json
import sqlite3
import os
# SQLlite connection
conn = sqlite3.connect("companies.db")
cur = conn.cursor()
# create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        city TEXT NOT NULL,
        address TEXT,
        rating REAL,
        reviews_count INTEGER DEFAULT 0,
        site TEXT,
        phone TEXT
    )
""")
conn.commit()
# ---------- 2. Download from JSON-files ----------
def load_json_files():
    records = []
    for filename in os.listdir("."):
        if filename.startswith("page_") and filename.endswith(".json"):
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("items", []):
                    rating = item.get("rating")
                    if isinstance(rating, str):
                        rating = rating.replace(",", ".")
                        try:
                            rating = float(rating)
                        except:
                            rating = None
                    records.append((
                        item.get("id"),
                        item.get("name"),
                        item.get("category"),
                        item.get("city"),
                        item.get("address"),
                        rating,
                        item.get("reviews_count", 0),
                        item.get("site"),
                        item.get("phone")
                    ))
    return records
records = load_json_files()
if not records:
    print("Нет данных для загрузки. Проверь, что файлы page_*.json лежат в папке.")
    exit()
cur.executemany("""
    INSERT OR REPLACE INTO companies
        (id, name, category, city, address, rating, reviews_count, site, phone)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", records)
conn.commit()
print(f" Загружено {len(records)} записей.")
# ---------- 3.analytical queries----------
print("\n" + "="*60)
print("1. Топ-5 категорий по числу компаний:")
cur.execute("""
    SELECT category, COUNT(*) AS company_count
    FROM companies
    GROUP BY category
    ORDER BY company_count DESC
    LIMIT 5
""")
for row in cur.fetchall():
    print(f"   {row[0]}: {row[1]}")
print("\n2. Средний рейтинг по городам:")
cur.execute("""
    SELECT city,
           ROUND(AVG(rating), 2) AS avg_rating,
           COUNT(*) AS company_count
    FROM companies
    WHERE reviews_count >= 10 AND rating IS NOT NULL
    GROUP BY city
    ORDER BY avg_rating DESC
""")
for row in cur.fetchall():
    print(f"   {row[0]}: {row[1]} (компаний: {row[2]})")
print("\n3. Доля компаний с сайтом по категориям:")
cur.execute("""
    SELECT category,
           COUNT(*) AS total,
           COUNT(site) AS with_site,
           ROUND(COUNT(site) * 100.0 / COUNT(*), 2) AS percent_with_site
    FROM companies
    GROUP BY category
    ORDER BY percent_with_site DESC
""")
for row in cur.fetchall():
    print(f"   {row[0]}: {row[3]}% (с сайтом: {row[2]} из {row[1]})")
print("\n" + "="*60)
print("База данных сохранена в файл companies.db.")
# close connection
conn.close()
