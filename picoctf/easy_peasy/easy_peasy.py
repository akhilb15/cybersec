a = 0x0345376e1e5406691d5c076c4050046e4000036a1a005c6b1904531d3941055d # encrypted flag
b = 0x0346303d1902033d1959003d1903553d1951553d1907593d1951511a3d190505 # a*32 encrypted
c = 0x6161616161616161616161616161616161616161616161616161616161616161 # a*32 not encrypted
# print('{:x}'.format(c^b^a)) # c^b gives key, key ^ a gives flag in hex 
print(bytes.fromhex('{:x}'.format(c^b^a)).decode("ASCII")) # flag in hex -> bytes -> ascii (which is the actual flag)
