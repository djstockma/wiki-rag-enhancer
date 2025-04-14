from utils.db import find_best_match
from utils.embedding import embed_text
from utils.db import get_connection

def find_matches(text):
    conn = get_connection()
    embedded = embed_text(text)
    result = find_best_match(conn, embedded)
    return result