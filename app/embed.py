import json
from sentence_transformers import SentenceTransformer
from utils.db import get_connection, insert_embedding, delete_embeddings
from utils.text_utils import chunk_text

def embed_articles(json_path="wiki_data/raw_wiki_content.json", language="en"):
    print(" Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print(f" Loading articles from {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(" Connecting to MariaDB...")
    conn = get_connection()

    print("Truncating old embedding table...")
    delete_embeddings(conn)

    for title, content in articles.items():
        print(f"\n Processing article: {title}")
        chunks = chunk_text(content, max_tokens=150)
        embeddings = model.encode(chunks, convert_to_numpy=True)
        print(embeddings.shape)
        for idx, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            insert_embedding(
                conn,
                title=title,
                chunk_index=idx,
                chunk_text=chunk,
                embedding=vector,
                language=language
            )

        print(f"Inserted {len(chunks)} chunks for '{title}'")

    conn.close()
    print("Embedding complete.")
