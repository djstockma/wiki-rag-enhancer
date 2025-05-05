from newspaper import Article
from utils.logging_config import get_logger

logger = get_logger()

def extract_article_text(url: str) -> str | None:
    logger.info(f"Extracting article from URL: {url}")
    article = Article(url)
    article.download()
    article.parse()
        
    logger.info(f"Article title: {article.title}")
    logger.info(f"Article authors: {article.authors}")
    logger.info(f"Article text length: {len(article.text)}")  # Log the first 100 characters
    if len(article.text) < 10:
        logger.error("Extracted article text is too short.")
        return None
    else:
        return article.text