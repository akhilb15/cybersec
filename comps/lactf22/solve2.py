import numpy as np
from sympy import Matrix
from pwn import *

def det(M):
    # stolen from https://stackoverflow.com/a/66192895
    M = [[int(x) for x in row] for row in M] # make a copy to keep original M unmodified
    N, sign, prev = len(M), 1, 1
    for i in range(N-1):
        if M[i][i] == 0: # swap with another row having nonzero i's elem
            swapto = next( (j for j in range(i+1,N) if M[j][i] != 0), None )
            if swapto is None:
                return 0 # all M[*][i] are zero => zero determinant
            M[i], M[swapto], sign = M[swapto], M[i], -sign
        for j in range(i+1,N):
            for k in range(i+1,N):
                assert ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) % prev == 0
                M[j][k] = ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) // prev
        prev = M[i][i]
    return sign * M[-1][-1]

n = 20
A = np.random.randint(0, 95, [n, n])
while np.gcd(det(A), 95) != 1:
    # ensures invertibility
    A = np.random.randint(0, 95, [n, n])

def stov(s):
    return np.array([ord(c)-32 for c in s])

def vtos(v):
    return ''.join([chr(v[i]+32) for i in range(n)])

def encrypt(s):
    return vtos(np.matmul(A, stov(s))%95)

def xorencrypt(s, fakeflag):
    v1 = stov(s)
    v2 = stov(fakeflag)
    v = np.bitwise_xor(v1, v2)
    return encrypt(vtos(v))

def xor(s1, s2):
    return vtos(np.bitwise_xor(stov(s1), stov(s2)))

    
fakeflag = "lactf{" + ''.join([chr(ord('a')+np.random.randint(0,26)) for _ in range(13)]) + "}"
    

# generate ascii plaintext strings of length n
p1 = ''.join([chr(np.random.randint(32, 127)) for i in range(n)])
p2 = ''.join([chr(np.random.randint(32, 127)) for i in range(n)])

c1 = xorencrypt(p1, fakeflag)
c2 = xorencrypt(p2, fakeflag)

print(p1)
print(c1)
print(p2)
print(c2)

# how do I get A using c1, c2, c3, p1, p2, p3?








