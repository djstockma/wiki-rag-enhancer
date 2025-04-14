import mariadb
import time
import sys
import requests
from fetch_wikipedia import fetch_pages
from embed import embed_articles

time.sleep(5) # Gives mariadb time to start



def main():
    #titles = ["Helsingfors", "Åbo", "Nykarleby", "Kokkola"]
    #fetch_pages(titles=titles)              # saves raw_wiki_content.json
    embed_articles()              # loads it and inserts into DB

if __name__ == "__main__":
    main()


