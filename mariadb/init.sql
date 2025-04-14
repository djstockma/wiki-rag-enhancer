CREATE TABLE IF NOT EXISTS test (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT,
    embedding VECTOR(4) NOT NULL
);

CREATE TABLE wiki_embeddings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    article_title VARCHAR(255),
    chunk_index INT,
    chunk_text TEXT,
    embedding VECTOR(384), -- assuming 384-dimensional embeddings
    language VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO test (content, embedding)
VALUES ("hello", VEC_FromText('[0.3, 0.5, 0.2, 0.1]'));