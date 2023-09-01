import requests

set = set()
url = "https://0ijq1i6sp1.execute-api.us-east-1.amazonaws.com/dev/stream"

# store characters in r.text in a set
for _ in range(100):
    r = requests.get(url)
    # trim '\n'
    c = r.text[:-1]
    set.add(c)
    
# print the set
print(set)


