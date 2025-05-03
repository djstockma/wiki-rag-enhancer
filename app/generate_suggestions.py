import openai
from utils import get_logger

logger = get_logger()

def suggest_wikipedia_additions(wiki_chunks: list[str], source_text: str, model="gpt-4o-mini") -> dict:
    """
    Uses GPT to compare Wikipedia content with a source and suggest new facts to add.

    Args:
        wiki_chunks (list[str]): Relevant chunks from Wikipedia.
        source_text (str): The source article (e.g. news article).
        model (str): OpenAI model to use, default is gpt-4.

    Returns:
        dict: JSON-parsed suggestions (structured output from GPT).
    """

    # Construct the input prompt
    joined_chunks = "\n\n".join(wiki_chunks)
    user_prompt = f"""Your task is to:
1. Compare the source text to the Wikipedia content.
2. Identify facts that are in the source but missing from the Wikipedia.
3. Output proposed additions in structured JSON format like this:
{{
  "proposed_additions": [
    {{
      "fact": "Short factual statement.",
      "justification": "Why it's relevant for the article.",
      "section_hint": "Optional: which section it fits into (if any)."
    }},
    ...
  ]
}}

Wikipedia content:
<<<
{joined_chunks}
>>>

Source text:
<<<
{source_text}
>>>"""

    # Send to OpenAI
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a factual assistant helping improve Wikipedia articles by comparing them "
                    "to reliable sources and identifying missing but relevant content."
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.3,  # Low temperature for reliability
    )

    # Extract and try to parse the structured response
    reply = response["choices"][0]["message"]["content"]

    # Try to safely parse JSON if it's well-formed
    import json
    try:
        start = reply.find("{")
        parsed = json.loads(reply[start:])
        return parsed
    except Exception as e:
        logger.warning("Warning: Could not parse JSON. Raw output:")
        logger.warning(reply)
        return {"error": "Failed to parse JSON", "raw_output": reply}
