def chunk_text(text, max_tokens=150):
    # Roughly split by sentence/paragraph
    chunks = []
    current = []
    token_count = 0

    for paragraph in text.split("\n"):
        if not paragraph.strip():
            continue

        tokens = paragraph.split()  # Simple word split
        if token_count + len(tokens) > max_tokens:
            chunks.append(" ".join(current))
            current = tokens
            token_count = len(tokens)
        else:
            current += tokens
            token_count += len(tokens)

    if current:
        chunks.append(" ".join(current))

    return chunks
