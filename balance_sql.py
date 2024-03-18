import psycopg2
import time

POSTGRES_USER = "postgres_user"
POSTGRES_PASSWORD = "postgres_password"
POSTGRES_HOST = "postgres_host" 
POSTGRES_PORT = "5432"

def monitor_load():
    conn = psycopg2.connect(dbname="postgres", user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM pg_stat_activity;")
    active_connections = cur.fetchone()[0]
    conn.close()
    print(f"Active connections: {active_connections}")
    return active_connections

def adjust_postgres_settings(active_connections):
    conn = psycopg2.connect(dbname="postgres", user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT)
    cur = conn.cursor()
    if active_connections > 100:
        print("Up max connections")
        cur.execute("ALTER SYSTEM SET max_connections = 200;")
        conn.commit()
        cur.execute("SELECT pg_reload_conf();")
        conn.commit()
    elif active_connections < 50:
        print("Down max connections")
        cur.execute("ALTER SYSTEM SET max_connections = 100;")
        conn.commit()
        cur.execute("SELECT pg_reload_conf();")
        conn.commit()
    conn.close()

while True:
    active_connections = monitor_load()
    adjust_postgres_settings(active_connections)
    time.sleep(60)