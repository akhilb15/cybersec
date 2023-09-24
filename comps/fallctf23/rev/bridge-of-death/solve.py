a = 0x796cb1915fa89cfd;
b = 0xbc231de9550ceebb;
c = 0xa743aa7d9151e4f3;
d = 0xb871d078f633fb51;
e = 0x79354c9e0e5432e;
f = 0xbdc7f84cbc54ddb9;
g = 0x171d06bbaa8c3faf;
h = 0xfdca0166;
i = 0xe1;

j = 0x215dfe62fcff58e;
k = 0xe35074b6216d86cc;
l = 0xf8319b1cce628c87;
m = 0xdd078f1cc5008b22;
n = 0x68cc2dbd89867342;
o = 0xd1a98d13d23582df;
p = 0x766a75e4c4bf5b9b;
q = 0x8aa56d57;
r = 0x9c;

nums = [a, b, c, d, e, f, g, h, i]

arr1 = []
for x in nums:
    while x > 0:
        arr1.append(x & 0xff)
        x >>= 8
        
nums2 = [j, k, l, m, n, o, p, q, r]
arr2 = []
for x in nums2:
    while x > 0:
        arr2.append(x & 0xff)
        x >>= 8
        
print(hex(len(arr1)))
print(hex(len(arr2)))


flag = []
for i in range(0x3d):
    flag.append(arr1[i] ^ arr2[i])
print(flag)

flag = ''.join([chr(x) for x in flag])
print(flag)