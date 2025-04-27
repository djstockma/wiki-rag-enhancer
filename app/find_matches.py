from utils.db import find_best_match, get_relevant_article_counts
from utils.embedding import embed_text
from utils.db import get_connection

def find_matches(text, n=1, articles: list[str] = []):
    """Returns list[id, text, embedding, article_title]"""
    conn = get_connection()
    embedded = embed_text(text)
    result = find_best_match(conn, embedded, n, articles)
    return result

def find_relevant_articles(text, n=1000):
    conn = get_connection()
    embedded = embed_text(text)
    counts = get_relevant_article_counts(conn, embedded, n=n)
    return counts