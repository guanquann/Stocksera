import sqlite3

conn = sqlite3.connect("database/database.db", check_same_thread=False)
db = conn.cursor()


def reset_trending_db():
    """
    Reset Stocksera trending table in database
    """
    db.execute("SELECT * FROM stocksera_trending ORDER BY count DESC LIMIT 10")
    top_10 = db.fetchall()

    db.execute("DELETE FROM stocksera_trending")

    count = 20
    for row in top_10:
        row = list(row)
        row[2] = count
        print(row)
        db.execute("INSERT OR IGNORE INTO stocksera_trending VALUES (?, ?, ?, ?)", tuple(row))
        conn.commit()
        count -= 1


if __name__ == '__main__':
    reset_trending_db()