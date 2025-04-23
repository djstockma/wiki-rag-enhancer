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
    with open("wiki_data/raw_wiki_content.json", "w") as f: #FIXME: for larger amounts of data, skip this in-between writing step!
        json.dump(pages, f, indent=2)


