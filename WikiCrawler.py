import time
import requests
import bs4
import urllib

#Script crawls Wikipedia from a random page, entering the first link of each page untill reaching Hitler (or a stop condition)

target_url = 'https://wikipedia.org/wiki/Adolf_Hitler'   
start_url='https://en.wikipedia.org/wiki/Special:Random'  

def find_first_link(url):
    # Function finds  first link of wiki page
    # We avoid footnoted by ignoring non-direct child a tags
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    url=soup.find(id='mw-content-text').find(class_="mw-parser-output") #HTML body
    link=None
    for element in url.find_all("p",recursive=False):                  #HTML Paragraphs avoiding tables using no recursive
        if element.find("a", recursive=False):                          #HTML link (If exists)
            link = element.find("a", recursive=False).get('href')       #looking at direcrt child links using no recursive
            break
    return urllib.parse.urljoin('https://en.wikipedia.org/', link)      #Makes the link whole

def continue_crawl(search_history,target_url,max_cycle=25):
#Stop conditions
    if search_history[-1]==target_url:                                  
        print ("Crawler reached the destination")
        return False
    elif len(search_history)>max_cycle:                                
        print("Crawler exceeded max page number")
        return False
    elif search_history[-1] in search_history[:-1]: 
        print("Crawler entered a loop")
        return False
    elif search_history[-1] == "https://en.wikipedia.org/": 
        print("Crawler reached a linkless page")
        return False
    return True

article_chain=[start_url]
while continue_crawl(article_chain, target_url):
    print(article_chain[-1])  #Print the visited pages
    first_link = find_first_link(article_chain[-1])
    article_chain.append(first_link)
    time.sleep(2) # delay for etiquette


