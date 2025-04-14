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
    #titles = ["Helsingfors", "Åbo", "Nykarleby", "Kokkola"]
    #fetch_pages(titles=titles)              # saves raw_wiki_content.json
    
    embed_articles()       # Go through the json, embed chunks and insert into db
    
    input_text = "One could mix up helsingfors and helsingborg, ending up in an old swedish city instead of a finnish one"
    result = find_matches(input_text)
    print(f"Here's the top result:") 
    print(f"Article name: {result[3]} \n\n Content: {result[1]}")

if __name__ == "__main__":
    main()


