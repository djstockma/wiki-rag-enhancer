import mariadb
import numpy as np
import os

def get_connection():
    print(os.getenv("DB_USER"))
    print(os.getenv("DB_PASS"))
    print(os.getenv("DB_HOST"))
    print(os.getenv("DB_PORT"))
    print(os.getenv("DB_NAME"))
    return mariadb.connect(
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "password"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME", "ragdb")
    )

def insert_embedding(conn, title, chunk_index, chunk_text, embedding, language="en"):
    cur = conn.cursor()
    # Convert vector to list or binary as needed
    if isinstance(embedding, np.ndarray):
        embedding = embedding.tolist()

    query = """
        INSERT INTO wiki_embeddings (article_title, chunk_index, chunk_text, embedding, language)
        VALUES (?, ?, ?, Vec_FromText(?), ?)
    """
    cur.execute(query, (title, chunk_index, chunk_text, embedding, language))
    conn.commit()
