import time
import streamlit as st
from fetch_wikipedia import fetch_pages
from find_matches import find_matches, find_relevant_articles

def main():
    st.set_page_config(page_title="Wikipedia RAG enhancer", layout="wide")
    st.title("Wikipedia RAG enhancer")

    st.header("Paste Source Text")
    source_text = st.text_area(
        "Paste the source you want to use for improvement here:", 
        height=400, 
        key="source_text"
    )

    st.sidebar.header("Settings")
    n_articles = st.sidebar.slider("How many articles to fetch", min_value=1, max_value=10, value=3, key="n_articles")
    n_chunks_per_article = st.sidebar.slider("How many chunks per article", min_value=1, max_value=50, value=2, key="n_chunks_per_article")

    if st.button("Check"):
        if not source_text.strip():
            st.warning("Please paste some text first!")
        else:
            # Find best articles
            occurances = find_relevant_articles(source_text, n=100)
            top_articles = sorted(occurances, key=occurances.get, reverse=True)[:n_articles]

            # Find matches per chunk
            grouped_matches = {}
            for article in top_articles:
                matches = find_matches(text=source_text, n_chunks=n_chunks_per_article, article=article)
                grouped_matches[article] = matches

            # Save matches in session state
            st.session_state.grouped_matches = grouped_matches
            st.session_state.selected_chunks = []  # Reset selected chunks

    # Now show matches if they exist
    if "grouped_matches" in st.session_state:
        st.header("Top Matching Wikipedia Chunks")

        for article_title, chunks in st.session_state.grouped_matches.items():
            st.subheader(f"{article_title}")

            for idx, chunk in enumerate(chunks, 1):
                chunk_text = chunk[1]
                chunk_id = f"{article_title}_{idx}"

                with st.expander(f"Chunk #{idx}"):
                    st.write(chunk_text)
                    if st.checkbox("Select this chunk", key=chunk_id):
                        selected = {
                            "article_title": article_title,
                            "chunk_text": chunk_text
                        }
                        if selected not in st.session_state.selected_chunks:
                            st.session_state.selected_chunks.append(selected)

        if st.button("Proceed with Selected Chunks"):
            if st.session_state.selected_chunks:
                st.success(f"{len(st.session_state.selected_chunks)} chunks selected!")
                st.write(st.session_state.selected_chunks)
            else:
                st.warning("Please select at least one chunk!")

if __name__ == "__main__":
    main()
