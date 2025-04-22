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
    
    input_text = "Helsinki (Helsingfors in Swedish) is the current capital of Finland, and it should not be confused with the Swedish city of Helsingborg, which is a city in south-western Sweden. Helsingborg, in fact, is closer to Denmark than Finland. Before Helsinki became capital, Turku was the capital of Finland, until it burned down."
    input_text = "Nykarleby is a bilingual municipality with Finnish and Swedish as its official languages. The population consists of 7% Finnish speakers, 84% Swedish speakers, and 10% speakers of other languages.\nThe largest employers in the town are Prevex (member of KWH Group), a packaging and piping products manufacturer, Westwood, which manufactures wooden staircases, and in the village of Jeppo, KWH Mirka"
    result = find_matches(input_text, 4) # Number of matches is optional, default=1
    print(f"Here are the top {len(result)} result(s):")
    for i, chunk in enumerate(result):
        print(f"Chunk {i + 1} (from article '{chunk[3]}'): {chunk[1]}")
    # print(f"Article name: {result[3]} \n\n Content: {result[1]}")

if __name__ == "__main__":
    main()


