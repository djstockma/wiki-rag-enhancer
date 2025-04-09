import mariadb
import time
import sys
import requests

time.sleep(10) # Gives mariadb time to start

try:
    # Test mariadb connection
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
    cur.execute("SELECT * FROM test")
    print(cur.fetchall())

    # Test wikipedia fetching
    def fetch_wikipedia_summary(title):
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("extract")
        else:
            return f"Error: {response.status_code}"
    summary = fetch_wikipedia_summary("Jens")
    print(summary)

except mariadb.Error as e:
    print(f"Attempt failed: Could not connect to MariaDB: {e}")

