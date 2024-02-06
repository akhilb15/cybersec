#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *


# exe = ELF('./chal')
# libc = ELF('./path/to/libc')
# ld = ELF('./path/to/ld')

{bindings} # for pwninit, replaces above

host = 'chal.sigpwny.com'
port = 1337

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-f', '-h']
context.binary = {bin_name}

# rop = ROP(exe)


# Run without randomization
# python3 solve.py GDB NOASLR

# To get libc and linker:
# ldd $(which ls) in docker
# docker cp the files


def conn(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug({proc_args}, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(host, port)
    else:
        return process({proc_args}, *a, **kw)

gdbscript = '''
b *main
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def solve():
    io = conn()

    # exploit code here

    io.interactive()
    
if __name__ == "__main__":
    solve()

