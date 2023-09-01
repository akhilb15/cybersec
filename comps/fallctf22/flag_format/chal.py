from Crypto.Random import get_random_bytes
import os

def xor(ciphertext, key):
    # cycle repeats the text infinitely
    from itertools import cycle
    return bytes(c^k for c,k in zip(ciphertext, cycle(key)))

# The output of this function has been written to message.txt
def main():
    flag = "sigpwny{this_is_a_fake_flag}"
    key = bytes(get_random_bytes(8))
    assert len(key) == 8
    
    print(xor(bytes(flag.encode()), key).hex())

if __name__ == '__main__':
    main()
