import os
def xor(a, b):
    """xor takes in two bytearrays and returns a list of integers"""
    return [c ^ d for c, d in zip(a, b)]

messages = [...]

key = os.urandom(1024)
ciphertexts = []
for m in messages:
    ciphertext = xor(bytes(m.encode("ascii")), key)
    ciphertexts.append(bytes(ciphertext).hex())

print(ciphertexts[0].strip("'"))
print("hi")
