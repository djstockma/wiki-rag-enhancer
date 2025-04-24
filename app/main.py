import mariadb
import time
import sys
import requests
from fetch_wikipedia import fetch_pages
from embed import embed_articles
from find_matches import find_matches, find_relevant_articles

time.sleep(4) # Gives mariadb time to start



def main():

    # For testing: this is commented out so the test data is used, and not fetched again every time
    #titles = ["Helsingfors", "Åbo", "Nykarleby", "Kokkola", "Mattlidens gymnasium", "Aalto university", "München", "Pope Franciskus", "Hotwheels"]
    #fetch_pages(titles=titles)              # saves raw_wiki_content.json
    
    embed_articles()       # Go through the json, embed chunks and insert into db
    
    input_text = "Here we can yap about cars and tracks, which should point tot hotwheels"
    result = find_matches(input_text, 4) # Number of matches is optional, default=1
    print(f"Here are the top {len(result)} result(s):")
    for i, chunk in enumerate(result):
        print(f"Chunk {i + 1} (from article '{chunk[3]}'): {chunk[1]}")
    # print(f"Article name: {result[3]} \n\n Content: {result[1]}")


    # Here we look at the n(=10) closest chunks, and see what article they belong to
    print("articles:")
    for key, value in find_relevant_articles(input_text, n=10).items():
        print(f"name: {key}, occurances: {value}")

if __name__ == "__main__":
    main()


