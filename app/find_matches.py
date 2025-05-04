from utils.db import find_best_matches, get_relevant_article_counts
from utils.embedding import embed_text
from utils.db import get_connection

def find_matches(text, n_chunks=1, article: str = None):
    """Fetches n matches for ONE article. Returns list[id, text, embedding, article_title, chunk_index, certainty]"""
    conn = get_connection()
    embedded = embed_text(text)
    if article:
        result = find_best_matches(conn, embedded, n_chunks, [article])
    else:
        result = find_best_matches(conn, embedded, n_chunks, [])
    return result

def find_relevant_articles(text, n=1000):
    conn = get_connection()
    embedded = embed_text(text)
    counts = get_relevant_article_counts(conn, embedded, n=n)
    return counts
