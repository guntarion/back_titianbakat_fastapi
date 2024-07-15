import sqlite3


def optimize_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("VACUUM")
    cursor.execute("REINDEX")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    optimize_database("./JaPoReporting.db")
