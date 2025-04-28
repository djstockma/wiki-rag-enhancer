import streamlit as st
from load_db import load_db
from find_matches import find_matches, find_relevant_articles

def main():
    st.set_page_config(page_title="Wikipedia RAG enhancer", layout="wide")
    st.title("Wikipedia RAG enhancer")

    st.header("Paste Source Text")
    source_text = st.text_area("Paste the source you want to use for improvement here:", height=400)

    st.sidebar.header("Settings")
    n_articles = st.sidebar.slider("How many articles to fetch", min_value=1, max_value=10, value=3)
    n_chunks_per_article = st.sidebar.slider("How many chunks per article", min_value=1, max_value=50, value=2)

    if st.sidebar.button("Run Embedding"):
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

        occurances = find_relevant_articles(source_text, n=100)
        top_articles = sorted(occurances, key=occurances.get, reverse=True)[:n_articles]

        grouped_matches = {}
        for article in top_articles:
            matches = find_matches(text=source_text, n_chunks=n_chunks_per_article, article=article)
            grouped_matches[article] = matches

        st.session_state.grouped_matches = grouped_matches
        st.session_state.selected_chunks = {}

    if st.session_state.grouped_matches:
        st.header("Top Matching Wikipedia Chunks")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select All"):
                for article_title, chunks in st.session_state.grouped_matches.items():
                    for idx, chunk in enumerate(chunks, 1):
                        key = f"{article_title}_{idx}"
                        st.session_state.selected_chunks[key] = True
                        st.session_state[key] = True  # Force checkbox to be checked
        with col2:
            if st.button("Deselect All"):
                for article_title, chunks in st.session_state.grouped_matches.items():
                    for idx, chunk in enumerate(chunks, 1):
                        key = f"{article_title}_{idx}"
                        if key in st.session_state.selected_chunks:
                            del st.session_state.selected_chunks[key]
                        st.session_state[key] = False  # Force checkbox to be unchecked

        for article_title, chunks in st.session_state.grouped_matches.items():
            st.subheader(f"{article_title}")
            for idx, chunk in enumerate(chunks, 1):
                chunk_text = chunk[1]
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
                            "chunk_text": chunk[1]
                        })

            if selected_data:
                st.success(f"{len(selected_data)} chunks selected!")
                st.write(selected_data)
            else:
                st.warning("Please select at least one chunk.")

if __name__ == "__main__":
    main()
