from sentence_transformers import SentenceTransformer

def embed_text(text: str):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding