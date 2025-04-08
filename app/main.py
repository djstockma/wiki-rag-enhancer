import mariadb
import time
import sys
import wikipedia

MAX_RETRIES = 10
RETRY_DELAY = 3  # seconds

for attempt in range(1, MAX_RETRIES + 1):
    try:
        conn = mariadb.connect(
            user="raguser",
            password="ragpass",
            host="mariadb",
            port=3306,
            database="ragdb"
        )
        print(" Connected to MariaDB!")
        cur = conn.cursor()
        cur.execute("SELECT 'Hello from MariaDB!'")
        print(cur.fetchone()[0])
        testvalue = wikipedia.summary("Wikipedia")
        print(testvalue)
        break  # Exit the loop if connection is successful

    except mariadb.Error as e:
        print(f"Attempt {attempt}: Could not connect to MariaDB: {e}")
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)
        else:
            print("Max retries reached, exiting.")
            sys.exit(1)
