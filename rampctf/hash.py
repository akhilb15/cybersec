import hashlib

SALT = "ada32db78873"
HASH = "48ded480c701abd932bb87f4998bf8ef"

# open wordlist file: word-list-7-letters.txt
# brute force md5(word + SALT) == HASH
with open("word-list-7-letters.txt", "r") as f:
    for line in f:
        word = line[:-1]
        if hashlib.md5((word + SALT).encode()).hexdigest() == HASH:
            print(word)
            exit()
        

