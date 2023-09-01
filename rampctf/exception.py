import requests 

url = "https://0ijq1i6sp1.execute-api.us-east-1.amazonaws.com/dev/exception?q="

# brute force using wordlist
with open("word-list-7-letters.txt", "r") as f:
    for line in f:
        word = line[:-1]
        if sum([ord(c) - 96 for c in word]) != 42: continue
        r = requests.get(url + word)
        if "File" not in r.text:
            print(word)
            print(r.text)
            exit()

    