import time
from fetch_wikipedia import fetch_pages
from embed import embed_articles
from find_matches import find_matches, find_relevant_articles

time.sleep(4) # Gives mariadb time to start



def main():

    # For testing: this is commented out so the test data is used, and not fetched again every time
    #titles = ["Helsingfors", "Åbo", "Nykarleby", "Kokkola", "Mattlidens gymnasium", "Aalto university", "München", "Pope Franciskus", "Hotwheels"]
    #fetch_pages(titles=titles)              # saves raw_wiki_content.json
    
    embed_articles()       # Go through the json, embed chunks and insert into db
    
    input_text = "Let's say i type something about esbo, which is a town in uusimaa. It also contains mattby. Where would this take me?"
    
    
    result = find_matches(input_text, 4) # Number of matches is optional, default=1
    print(f"Here are the top {len(result)} result(s):")
    for i, chunk in enumerate(result):
        print(f"Chunk {i + 1} (from article '{chunk[3]}'): {chunk[1]}")
    # print(f"Article name: {result[3]} \n\n Content: {result[1]}")


    # Article selection:
    # Here we can first select k relevant articles based off how relevant they seem to the source, and then proceed using only those articles
    k = 1 # Number of articles we want to compare two
    n = 10 # Number of occurances to look at when looking for top occuring articles
    
    print("articles:")
    occurances = find_relevant_articles(input_text, n=n)
    for key, value in occurances.items():                       
        print(f"name: {key}, occurances: {value}")

    # Now, let's find the top chunks ONLY from the most relevant article(s)
    top_articles = sorted(occurances, key=occurances.get, reverse=True)[:k]
    relevant_chunks = find_matches(input_text, n=1, articles=top_articles)
    print(f"The top chunks were: {','.join(chunk[1] for chunk in relevant_chunks)}")

if __name__ == "__main__":
    main()


