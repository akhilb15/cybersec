from secrets import token_bytes
from itertools import cycle

ct_file = open("cipher.bin", "rb")

ct = ct_file.read()
# The XOR operation is symmetric, so we can use the same function to decrypt the ciphertext
png_magic_bytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"

#xor first 8 bytes of ct with png magic bytes
XOR = lambda a, b: bytes([i ^ j for i, j in zip(a, cycle(b))])
key = XOR(ct[:8], png_magic_bytes)
print(key)

# use key to recreate flag.png
flag = XOR(ct, key)
flag_file = open("flag.png", "wb")
flag_file.write(flag)
