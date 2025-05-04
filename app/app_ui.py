import streamlit as st
from load_db import load_db
from find_matches import find_matches, find_relevant_articles
from generate_suggestions import suggest_wikipedia_additions

def main():
    st.set_page_config(page_title="Wikipedia RAG enhancer", layout="wide")
    st.title("Wikipedia RAG enhancer")

    st.header("Paste Source Text")
    source_text = st.text_area("Paste the source you want to use for improvement here:", height=400)

    st.sidebar.header("Settings")
    n_articles = st.sidebar.slider("How many articles to fetch", min_value=1, max_value=10, value=3)
    n_chunks_per_article = st.sidebar.slider("How many chunks per article", min_value=1, max_value=50, value=2)

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
                chunk_certainty = chunk[4]
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
                            "chunk_text": chunk[1]
                        })

            if not selected_data:
                st.warning("Please select at least one chunk.")
            else:
                article_titles = list(set(d["article_title"] for d in selected_data))
                if len(article_titles) > 1:
                    st.error("Please select chunks from only one article.")
                    return

                article_title = article_titles[0]
                context_chunks = [d["chunk_text"] for d in selected_data]

                with st.spinner("Generating LLM suggestions..."):
                    suggestions = suggest_wikipedia_additions(
                        wiki_chunks=context_chunks,
                        source_text=source_text,
                    )

                st.success("Suggestions generated!")
                st.subheader("Suggested Additions to Wikipedia")
                st.write(suggestions)

if __name__ == "__main__":
    main()
