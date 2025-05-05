from openai import OpenAI
import os
from dotenv import load_dotenv
from utils.logging_config import get_logger

load_dotenv()
logger = get_logger()

def suggest_wikipedia_additions(wiki_chunks: list[dict], source_text: str, model="gpt-4o-mini") -> list[dict]:
    """
    Uses GPT to compare Wikipedia content with a source and suggest new facts to add.

    Args:
        wiki_chunks (list[dict]): Relevant chunks from Wikipedia with their metadata.
            (id, text, embedding, article_title, chunk_index, certainty)
        source_text (str): The source article (e.g. news article).
        model (str): OpenAI model to use, default is gpt-4.

    Returns:
        dict: JSON-parsed suggestions (structured output from GPT).
    """

    # Combining the Wikipedia chunks and metadata
    joined_chunks = ""
    for chunk in wiki_chunks:
        # Extract the chunk text and metadata
        chunk_text = chunk["chunk_text"]
        chunk_number = chunk["chunk_id"]
        chunk_title = chunk["article_title"]
        # Format the chunk with its metadata
        joined_chunks += f"#### Chunk {chunk_number} \n Title and subtitle: {chunk_title} \n Chunk Text: \n{chunk_text}\n\n"
    
    # Construct the input prompt
    user_prompt = f"""Your task is to:
1. Compare the source text to the Wikipedia content chunks.
2. Identify facts that are in the source but missing from the Wikipedia.
3. Output proposals for new text in structured JSON format like this:
{{
  "proposed_additions": [
    {{
      "chunk_title": "(Sub)title of the chunk",
      "chunk_id": "id of modified chunk, just the number (eg. "25")",
      "improved_chunk": "Original chunk text modified with added improvement.",
      "justification": "Why it's relevant for the article.",
      "section_hint": "Optional: which section it fits into (if any)."
    }},
    ...
  ]
}}

Please don't remove anything from the Wikipedia content, only make additions and return the improved chunk text (don't return the subtitle).

Wikipedia content:
<<<
{joined_chunks}
>>>

Source text:
<<<
{source_text}
>>>"""
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    # Send to OpenAI
    response = client.responses.create(
        model=model,
        instructions="You are a factual assistant helping improve Wikipedia articles by comparing them "
                      "to reliable sources and identifying missing but relevant content. "
                      "You generate the answers in the same language as the input, and adher to linguistic conventions of wikipedia.",
        input=user_prompt
    )

    # Extract and try to parse the structured response
    reply = response.output_text

    # Try to safely parse JSON if it's well-formed
    import json
    try:
        start = reply.find("{")
        end = reply.rfind("}")
        trimmed = reply[start:end + 1]
        parsed: dict = json.loads(trimmed)
        additions: list[dict] = parsed.get("proposed_additions")
        final_additions = []
        for addition in additions:
            # Ensure all required fields are present
            if "chunk_id" not in addition or "improved_chunk" not in addition or "justification" not in addition:
                logger.warning("Warning: Missing required fields in JSON response.") 
                continue
            
            # Add original chunk text for reference
            chunk_id_raw = addition["chunk_id"]
            try:
                chunk_id = int(chunk_id_raw)
            except ValueError:
                logger.warning(f"Invalid chunk_id value: {chunk_id_raw}")
                continue

            # Find matching chunk from wiki_chunks (assumes chunk_index is at index 4)
            (original_chunk, edit_url) = next(
                ((chunk["chunk_text"], chunk["edit_url"]) for chunk in wiki_chunks if int(chunk["chunk_id"]) == chunk_id),
                None
            )
            if original_chunk is None:
                logger.warning(f"No matching original chunk found for chunk_id={chunk_id}")
                continue
            
            addition["original_chunk"] = original_chunk
            addition["edit_url"] = edit_url
            final_additions.append(addition)

        return final_additions
    
    except ValueError as ve:
        logger.warning("Warning: Could not parse JSON due to value missing.")
        return []    
    except Exception as e:
        logger.warning("Warning: Could not parse JSON.")
        return []
