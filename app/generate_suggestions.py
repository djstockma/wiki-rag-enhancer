from openai import OpenAI
import os
from dotenv import load_dotenv
from utils.logging_config import get_logger

load_dotenv()
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
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    # Send to OpenAI
    response = client.responses.create(
        model=model,
        instructions="You are a factual assistant helping improve Wikipedia articles by comparing them "
                      "to reliable sources and identifying missing but relevant content. "
                      "You generate the answers in the same language as the input.",
        input=user_prompt
    )

    # Extract and try to parse the structured response
    logger.info(response.output_text)
    reply = response.output_text

    # Try to safely parse JSON if it's well-formed
    import json
    try:
        start = reply.find("{")
        end = reply.rfind("}")
        trimmed = reply[start:end + 1]
        parsed = json.loads(trimmed)
        return parsed
    except Exception as e:
        logger.warning("Warning: Could not parse JSON.")
        return {"error": "Failed to parse JSON", "raw_output": reply, "trimmed": trimmed}
