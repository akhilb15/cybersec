#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *


exe = ELF('./path/to/binary')
host = 'chal.sigpwny.com'
port = 1337

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
        return process([exe] + argv, *a, **kw)

gdbscript = '''
b *main
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def solve():
    io = conn()

    # shellcode = asm(shellcraft.sh())
    # payload = fit({
    #     32: 0xdeadbeef,
    #     'iaaa': [1, 2, 'Hello', 3]
    # }, length=128)
    # io.send(payload)
    # flag = io.recv(...)
    # log.success(flag)

    io.interactive()
    
if __name__ == "__main__":
    solve()

