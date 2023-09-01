plaintext = b'Cacturne-Grass-Dark'
ciphertext = b'kz\xc6\xb9\xd9Du\xcb\x8a\x9e\xe0\x9d\xbeo\xee\x03\xcf\xddd'
key = b''.join([(x ^ y).to_bytes(1,'big') for (x,y) in zip(plaintext,ciphertext)])
print(key)
encrypted_passwords = open("encrypted_passwords.txt", "rb").read().strip().split(b'\n')
for p in encrypted_passwords:
    print(b''.join([(x ^ y).to_bytes(1,'big') for (x,y) in zip(p,key)]))






