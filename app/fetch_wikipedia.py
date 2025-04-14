import wikipedia
import json
import os

def fetch_pages(titles, lang="en"):
    wikipedia.set_lang(lang)
    pages = {}
    for title in titles:
        try:
            page = wikipedia.page(title)
            pages[title] = page.content
        except Exception as e:
            print(f"Error fetching '{title}': {e}")
    return pages


