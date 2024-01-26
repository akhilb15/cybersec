from itertools import cycle

s = 'bctf'

f = '01:10:d0:10:42:41:34:20:b5:40:03:30:91:c5:e1:e3:d2:a2:72:d1:61:d0:10:e3:a0:43:c1:01:10:b1:b1:b0:b1:40:09'

flag_enc = [int(x, 16) for x in f.split(':')]
st = [ord(x) for x in s]

key = [x ^ y for x, y in zip(flag_enc, st)]
print(key)
flag = [x ^ y for x, y in zip(flag_enc, cycle(key))]
print(''.join([chr(x) for x in flag]))
     
    
    
    
    
        
    