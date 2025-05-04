import difflib
import re

def split_sentences(text: str) -> list[str]:
    # Split text into sentences (naive method)
    return re.split(r'(?<=[.!?])\s+', text.strip())

def generate_markdown_diff(original: str, improved: str) -> str:
    """
    Generate a granular markdown diff between original and improved texts
    with Streamlit-compatible syntax highlighting.
    """
    # Break text into smaller comparable units (sentences)
    original_sentences = split_sentences(original)
    improved_sentences = split_sentences(improved)

    # Create diff
    diff = difflib.ndiff(original_sentences, improved_sentences)

    # Format for markdown with `diff` block
    formatted_lines = []
    for line in diff:
        if line.startswith('+'):
            formatted_lines.append(f'+ {line[2:]}')
        elif line.startswith('-'):
            formatted_lines.append(f'- {line[2:]}')
        elif line.startswith('  '):
            formatted_lines.append(f'  {line[2:]}')  # unchanged

    return f"```diff\n" + "\n".join(formatted_lines) + "\n```"
