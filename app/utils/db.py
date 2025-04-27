import mariadb
import numpy as np
import os
import json

def get_connection():
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


def delete_embeddings(conn): #FIXME: this is not a god solution for prod maybe :)
    cur = conn.cursor()

    query = """
        TRUNCATE TABLE wiki_embeddings
    """
    cur.execute(query)
    conn.commit()


def find_best_match(conn, user_vector, n, articles: list[str] = []) -> list[(str, str, str, str)]:
    cursor = conn.cursor()

    vector_str = json.dumps(user_vector.tolist())
    params = []
    article_filter = ""
    if articles:
        placeholders = ','.join('?' for _ in articles)
        article_filter = f"WHERE article_title IN ({placeholders})"
        params.extend(articles)
    params.append(vector_str)

    query = f"""
        SELECT id, chunk_text, embedding, article_title
        FROM wiki_embeddings
        {article_filter}
        ORDER BY VEC_DISTANCE_COSINE(embedding, VEC_FromText(?))
        LIMIT {n}
    """

    cursor.execute(query, params)  # Pass vector as string, and also article names
    result = cursor.fetchall()

    conn.close()
    return result

def get_relevant_article_counts(conn, user_vector, n: int = 1000) -> dict[str, int]:
    """Returns a dict mapping where the key is the article name, 
    and the value is the number of appearances"""
    #FIXME: add normalisation based on number of article chunks somewhere?
    cursor = conn.cursor()
    dict = {}
    vector_str = json.dumps(user_vector.tolist())
    query = f"""
        SELECT id, chunk_text, embedding, article_title
        FROM wiki_embeddings
        ORDER BY VEC_DISTANCE_COSINE(embedding, VEC_FromText(?))
        LIMIT {n}
    """
    cursor.execute(query, [vector_str])
    rows = cursor.fetchall()

    for row in rows:
        title = row[3]
        if title in dict:
            dict[title] = dict[title] + 1
        else:
            dict [title] = 1
    
    return dict
