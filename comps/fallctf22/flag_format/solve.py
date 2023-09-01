# simple xor
def xor(ciphertext, key):
    # cycle repeats the text infinitely
    from itertools import cycle
    return bytes(c^k for c,k in zip(ciphertext, cycle(key)))

ct = bytes.fromhex("92d51d68f2d78e678fd30d47fcd682438ad2156fdacd9f79becc1679ecd7837999c807")
key1 = "sigpwny{"
key2 = xor(ct, bytes(key1.encode())).hex()
print(key2)

key = "e1bc7a1885b9f71c" # first 8 bytes (16 hex characters), since the key is 8 bytes long
flag = xor(ct, bytes.fromhex(key)).decode('utf-8')
print(flag)
