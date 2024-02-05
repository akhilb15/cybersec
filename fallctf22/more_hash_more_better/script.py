import hashlib
map = {}
flag = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV{}0123456789_"
for c in flag:
    h = hashlib.sha256()
    h.update(c.encode())
    map[h.hexdigest()] = c

hashes = open("hashes.txt").read().strip().split('\n')
for hash in hashes:
    print(map[hash], end='')
