#!/usr/bin/env python3
from pwn import *

# You may need to install pwntools to execute this script
# Do it with "python3 -m pip install pwntools"

# Remote = connect to remote server
# Process = run it locally
# Uncomment whichever one you want!
conn = remote('chal.sigpwny.com', 1352)
#conn = process('./stack1')

# Read through the first line from the program
conn.recvline() # This is SIGPwny stack1, go

# Step 1: Overflow the 'buf' variable
buf = b'A' * ??

# Step 2: Don't change the 'dontchangethis' variable!
# dontchangethis is a 32-bit integer, and since we're on x86 its stored little-endian
# We can put a 32 bit little endian address into our buffer using the p32() command from pwntools
buf += p32(??)

# Step 3: Change the 'changethis' variable!
buf += p32(??)

# Send the exploit & profit??
conn.sendline(buf)

# Never forget to go interactive!!!!
conn.interactive()
