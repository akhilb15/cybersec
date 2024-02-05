import requests
from bs4 import BeautifulSoup

url = 'http://web.chal.csaw.io:5010'
s = requests.session() # use session to persist cookies across requests, regular requests.get creates a new session every time
r = s.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

path = ""

while True:
    # if the flag is on the page then print it and break
    if "CTF" in r.text:
        print(r.text)
        break

    # find the link that actually works
    for link in soup.find_all("a"):
        p = link.get("href")

        if p != None:
            path = p
            print("Depth: " + path)
            break
    
    # go to new link
    r = s.get(url + path)
    soup = BeautifulSoup(r.text, 'html.parser')





