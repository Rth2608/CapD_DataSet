import psycopg2
import os

def save_to_db(news_items):
    conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_news (
            id SERIAL PRIMARY KEY,
            ticker TEXT,
            title TEXT,
            url TEXT,
            content TEXT,
            published_at TEXT
        )
    """)

    for news in news_items:
        cur.execute(
            "INSERT INTO stock_news (ticker, title, url, content, published_at) VALUES (%s, %s, %s, %s, %s)",
            (news["ticker"], news["title"], news["url"], news["content"], news["date"])
        )

    conn.commit()
    cur.close()
    conn.close()
