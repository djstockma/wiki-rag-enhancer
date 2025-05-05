import mariadb
import numpy as np
import os
import json
from dotenv import load_dotenv

from utils.logging_config import get_logger
logger = get_logger()

load_dotenv()

def get_connection():
    return mariadb.connect(
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "password"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME", "ragdb")
    )


def insert_embedding(conn, title, chunk_index, chunk_text, embedding, language="en", edit_url=""):
    cur = conn.cursor()
    # Convert vector to list or binary as needed
    if isinstance(embedding, np.ndarray):
        embedding = embedding.tolist()

    query = """
        INSERT INTO wiki_embeddings (article_title, chunk_index, chunk_text, embedding, language, edit_url)
        VALUES (?, ?, ?, Vec_FromText(?), ?, ?)
    """
    cur.execute(query, (title, chunk_index, chunk_text, embedding, language, edit_url))
    conn.commit()


def delete_embeddings(conn): #FIXME: this is not a god solution for prod maybe :)
    cur = conn.cursor()

    query = """
        TRUNCATE TABLE wiki_embeddings
    """
    cur.execute(query)
    conn.commit()



def find_best_matches(conn, user_vector, n, articles: list[str] = []):

    cursor = conn.cursor()

    vector_str = json.dumps(user_vector.tolist())
    params = []
    params.append(vector_str) # For SELECT
    article_filter = ""
    if articles:
        placeholders = ','.join('?' for _ in articles)
        article_filter = f"WHERE article_title IN ({placeholders})"
        params.extend(articles) # For WHERE IN clause
    params.append(vector_str) # For ORDER BY
    query = f"""
        SELECT id, chunk_text, embedding, article_title, chunk_index,
            1 - VEC_DISTANCE_COSINE(embedding, VEC_FromText(?)) AS certainty, edit_url
        FROM wiki_embeddings
        {article_filter}
        ORDER BY VEC_DISTANCE_COSINE(embedding, VEC_FromText(?))
        LIMIT {n}
    """
    cursor.execute(query, params)  # Pass vector as string, and also article names
    result = cursor.fetchall()
    result_sorted = sorted(result, key=lambda x: (x[3], x[0]))  # (article_title, id)
    conn.close()
    return result_sorted


def get_relevant_article_counts(conn, user_vector, n: int = 1000):
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
