import wikipediaapi
import time
from sentence_transformers import SentenceTransformer
import torch
from utils.db import get_connection, insert_embedding, delete_embeddings
from utils.text_utils import chunk_text
import pandas as pd
from utils.logging_config import get_logger

torch.classes.__path__ = [] # Fixes error: Tried to instantiate class '__path__._path', but it does not exist! Ensure that it is registered via torch::class_

logger = get_logger()

def get_titles(file_path: str) -> list:
    print(f"Reading file and 'Wikidata' column: {file_path}")
    df = pd.read_csv(file_path)
    wikidata_list = df['title'].tolist()
    logger.info(f"Found {len(wikidata_list)} items in 'Wikidata' column")
    return wikidata_list


def embed_articles(conn, pages: dict, model, language="en") -> int:
    for title, content in pages.items():
        chunks = chunk_text(content)
        embeddings = model.encode(chunks, convert_to_numpy=True)
        for idx, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            insert_embedding(
                conn,
                title=title,
                chunk_index=idx,
                chunk_text=chunk,
                embedding=vector,
                language=language
            )

    return(len(pages.items()))


def fetch_pages_batch(titles, lang="en", batch_size=100, sleep_time=0.5) -> int:
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='wiki_rag_enhancer (jens.w.stockmann@gmail.com)', language=lang)
    total_pages = len(titles)

    # Connect and delete old embeddings
    logger.info(" Connecting to MariaDB...")
    conn = get_connection()
    logger.info("Truncating old embedding table...")
    delete_embeddings(conn)
    total = 0
    logger.info("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    for start_idx in range(0, total_pages, batch_size):
        end_idx = min(start_idx + batch_size, total_pages)
        batch_titles = titles[start_idx:end_idx]

        pages = {}
        for title in batch_titles:
            page = wiki_wiki.page(title)
            if page.exists():
                pages[title] = page.text
                total += 1
            else:
                logger.info(f"Page not found: {title}")

        # Here you would insert `pages` into your database
        embed_articles(conn=conn, model=model, pages=pages, language=lang)

        logger.info(f"{total} pages total in database.")

        time.sleep(sleep_time)  # polite sleep after every batch so calls are spread out

    conn.close()
    logger.info("Embedding complete.")
    return total_pages


def load_db() -> int:
    titles = get_titles(file_path="wiki_data/articles_test.csv")
    return fetch_pages_batch(titles, lang="fi")















