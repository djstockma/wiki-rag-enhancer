-- This SQL script initializes the database for storing wiki embeddings.
CREATE TABLE wiki_embeddings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    article_title VARCHAR(255),
    chunk_index INT,
    chunk_text TEXT,
    embedding VECTOR(384), -- assuming 384-dimensional embeddings
    language VARCHAR(10),
    edit_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
