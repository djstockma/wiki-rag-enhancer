def chunk_text(text, min_words=50, max_words=150, overlap_words=20) -> list:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_chunk = []
    current_word_count = 0

    for paragraph in paragraphs:
        words = paragraph.split()

        # If paragraph too large, split it
        while len(words) > max_words:
            chunk_words = words[:max_words]
            chunks.append(" ".join(chunk_words))
            # Start next chunk with overlap
            words = words[max_words - overlap_words:]

        # Merge paragraphs
        if current_word_count + len(words) <= max_words:
            current_chunk.extend(words)
            current_word_count += len(words)
        else:
            if current_word_count >= min_words:
                chunks.append(" ".join(current_chunk))
                # Start new chunk with overlap from previous
                current_chunk = current_chunk[-overlap_words:] + words
                current_word_count = len(current_chunk)
            else:
                current_chunk.extend(words)
                current_word_count += len(words)

    # Final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
