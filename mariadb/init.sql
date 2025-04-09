CREATE TABLE IF NOT EXISTS test (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT,
    embedding VECTOR(4) NOT NULL
);

INSERT INTO test (content, embedding)
VALUES ("hello", VEC_FromText('[0.3, 0.5, 0.2, 0.1]'));