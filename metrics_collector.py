import psutil
import time
import sqlite3

DATABASE_NAME = 'metrics.db'

def collect_metrics(interval=10):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    while True:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk_io = psutil.disk_io_counters().read_bytes + psutil.disk_io_counters().write_bytes
        net_io = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        
        cursor.execute("INSERT INTO metrics (timestamp, cpu, memory, disk_io, network_io) VALUES (?, ?, ?, ?, ?)",
                       (timestamp, cpu, memory, disk_io, net_io))
        conn.commit()
        time.sleep(interval - 1)

if __name__ == "__main__":
    collect_metrics()