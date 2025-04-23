import mariadb
import time
import sys
import requests
from fetch_wikipedia import fetch_pages
from embed import embed_articles
from find_matches import find_matches

time.sleep(4) # Gives mariadb time to start



def main():

    # For testing: this is commented out so the test data is used, and not fetched again every time
    #titles = ["Helsingfors", "Åbo", "Nykarleby", "Kokkola", "Mattlidens gymnasium", "Aalto university", "München", "Pope Franciskus", "Hotwheels"]
    #fetch_pages(titles=titles)              # saves raw_wiki_content.json
    
    #embed_articles()       # Go through the json, embed chunks and insert into db
    
    input_text = "Some random yappayappa about the pope and the vatican city. The catholic church. May Pope franciskus rest in peace."
    result = find_matches(input_text, 4) # Number of matches is optional, default=1
    print(f"Here are the top {len(result)} result(s):")
    for i, chunk in enumerate(result):
        print(f"Chunk {i + 1} (from article '{chunk[3]}'): {chunk[1]}")
    # print(f"Article name: {result[3]} \n\n Content: {result[1]}")

if __name__ == "__main__":
    main()


