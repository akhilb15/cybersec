
# let flagEncrypted = [208, 17, 54, 47, 225, 72, 81, 62, 134, 78, 83, 55, 211, 110, 87];
# let flag = '';
# for (let i = 0; i < flagEncrypted.length; i++) {
#     flag += String.fromCharCode(flagEncrypted[i] ^ nums[i % nums.length]);
# }

# flagEncrypted = [208, 17, 54, 47, 225, 72, 81, 62, 134, 78, 83, 55, 211, 110, 87]
# flag = ''
# for i in range(len(flagEncrypted)):
#     flag += chr(flagEncrypted[i] ^ nums[i % len(nums)])


i = 0xb2
for j in range(-0x100, 0x100):
    for k in range(-0x100, 0x100):
        for m in range(-0x100, 0x100):
            acc = 0
            acc = acc | i & 0xff;
            acc = acc | (j & 0xff) << 8;
            acc = acc | acc << 16;
            acc = acc ^ (k & 0xff) << 13;
            acc = acc ^ (m & 0xff) << 49;
            if acc == 543056050:
                print(i, j, k, m)
                nums = [i, j, k, m]
                flagEncrypted = [208, 17, 54, 47, 225, 72, 81, 62, 134, 78, 83, 55, 211, 110, 87]
                flag = ''
                for i in range(len(flagEncrypted)):
                    flag += chr(flagEncrypted[i] ^ nums[i % len(nums)])
                print('sigpwny{' + flag + '}')
        

i = 0xb2
j = 0xcf
k = 0xd4
m = 0xea
              
acc = 0
acc = acc | i & 0xff;
acc = acc | (j & 0xff) << 8;
acc = acc | acc << 16;
acc = acc ^ (k & 0xff) << 13;
acc = acc ^ (m & 0xff) << 49;  

print(hex(acc))     


