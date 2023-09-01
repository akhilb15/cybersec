cipher_arr = [51, 105, 231, 176, 55, 46, 185, 187, 50, 225, 174, 228, 111, 237, 223, 105, 51, 174, 180, 95, 33, 181, 52, 239, 45, 97, 52, 41, 163, 97, 172, 236, 249, 31, 51, 37, 163, 181, 242, 229, 253]
flag = ""
for c in cipher_arr:

    # if (c & 128): c ^= 128 # if first bit was changed to 1 then make it 0
    # if (not (c & 64)): c ^= 64 # if second bit was changed to 0 then make it 1 (bc lowercase ascii letters are > 64)

    # a bit cleaner/more elegant
    c &= 63 # makes all changes to first two bits 0 (ex: 11101010 -> 00101010)
    c ^= 64 # adds back second bit (bc lowercase ascii letters are > 64)
    flag += chr(c)

print(flag)
