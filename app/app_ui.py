import streamlit as st
from load_db import load_db
from find_matches import find_matches, find_relevant_articles
from generate_suggestions import suggest_wikipedia_additions
from utils.logging_config import get_logger
from utils.generate_markdown_diff import generate_markdown_diff
from utils.parse_article import extract_article_text

logger = get_logger()

def main():
    st.set_page_config(page_title="Wikipedia RAG enhancer", layout="wide")
    st.title("Wikipedia RAG enhancer")

    st.header("Paste Source Text or URL (http:// or https://) here")  
    source_text = st.text_area("Paste the source you want to use for improvement here:", height=400)

    st.sidebar.header("Settings")
    n_chunks_per_article = st.sidebar.slider("How many chunks to fetch", min_value=1, max_value=100, value=20)

    st.sidebar.subheader("Wikipedia and embedding")
    if st.sidebar.button("Load data from wikipedia and Embed"):
        with st.spinner("Embedding Wikipedia articles..."):
            n_of_embedded_articles = load_db()
        st.sidebar.success(f"Embedding complete! {n_of_embedded_articles} articles embedded")
    if "selected_chunks" not in st.session_state:
        st.session_state.selected_chunks = {}

    if "grouped_matches" not in st.session_state:
        st.session_state.grouped_matches = {}

    if st.button("Check"):
        if not source_text:
            st.warning("Please paste some text first!")
            return
        
        if source_text.startswith("http://") or source_text.startswith("https://"):
            try:
                source_text = extract_article_text(source_text)
                if source_text:
                    st.success("Article content successfully extracted.")
                    st.subheader("Extracted Article Content:")
                    st.write(f"{source_text[0:200]}...")  # Display first 100 characters
                else:
                    st.error(f"Failed to extract article: {e}")
                    source_text = ""
                    return
            except Exception as e:
                st.error(f"Failed to extract article: {e}")
                source_text = ""
                return
            
        grouped_matches = {}
        matches = find_matches(text=source_text, n_chunks=n_chunks_per_article)
        for match in matches:
            article_title = match[3]
            if article_title not in grouped_matches:
                grouped_matches[article_title] = []
            grouped_matches[article_title].append(match) #FIXME: find a way to sort appearance of chunks!

        st.session_state.grouped_matches = grouped_matches
        st.session_state.selected_chunks = {}

    if st.session_state.grouped_matches:
        st.header("Top Matching Wikipedia Chunks")

        for article_title, chunks in st.session_state.grouped_matches.items():
            st.subheader(f"{article_title}")
            for idx, chunk in enumerate(chunks, 1):
                chunk_text = chunk[1]
                chunk_certainty = chunk[5]
                chunk_number = chunk[4]
                st.markdown(f"#### Chunk {chunk_number} (Certainty: {chunk_certainty:.2f})")
                key = f"{article_title}_{idx}"

                # Default value depends on session_state
                checkbox_val = st.checkbox("Select this chunk", key=key, value=st.session_state.get(key, False))

                if checkbox_val:
                    st.session_state.selected_chunks[key] = True
                else:
                    if key in st.session_state.selected_chunks:
                        del st.session_state.selected_chunks[key]

                st.write(chunk_text)

        if st.button("Proceed with Selected Chunks"):
            selected_data = []
            for article_title, chunks in st.session_state.grouped_matches.items():
                for idx, chunk in enumerate(chunks, 1):
                    key = f"{article_title}_{idx}"
                    if st.session_state.selected_chunks.get(key):
                        selected_data.append({
                            "article_title": article_title,
                            "chunk_text": chunk[1],
                            "chunk_index": chunk[4],
                            "chunk_id": chunk[0],
                            "edit_url": chunk[6],
                        })
            if not selected_data:
                st.warning("Please select at least one chunk.")
            else:
                with st.spinner("Generating LLM suggestions..."):
                    suggestions = suggest_wikipedia_additions(
                        wiki_chunks=selected_data,
                        source_text=source_text,
                    )

                st.success("Suggestions generated!")
                st.subheader("Suggested Additions to Wikipedia")
                for suggestion in suggestions:
                    diff_markdown = generate_markdown_diff(
                        suggestion["original_chunk"],
                        suggestion["improved_chunk"]
                    )
                    st.markdown(diff_markdown)
                    st.markdown(f"**Justification:** {suggestion['justification']}    **Edit [here]({suggestion['edit_url']})**")

                    # Uncomment if you want to see the full suggestion
                    #st.write(suggestion)

if __name__ == "__main__":
    main()
