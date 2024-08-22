import sqlite3

DATABASE_NAME = 'metrics.db'

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS metrics (
                        timestamp TEXT, 
                        cpu REAL, 
                        memory REAL,
                        disk_io REAL,
                        network_io REAL)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized and table created successfully.")