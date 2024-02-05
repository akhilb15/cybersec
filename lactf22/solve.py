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

def stov(s):
    return np.array([ord(c)-32 for c in s])

def vtos(v):
    return ''.join([chr(v[i]+32) for i in range(n)])

def encrypt(A, s):
    return vtos(np.matmul(A, stov(s))%95)


n = 20

# create invertible plaintext matrix
pt_matrix = np.random.randint(0, 95, [n, n])
while np.gcd(det(pt_matrix), 95) != 1:
    # ensures invertibility
    pt_matrix = np.random.randint(0, 95, [n, n])

# generate plaintext strings from matrix
plaintexts = [vtos(pt_matrix[i]) for i in range(n)]
ciphertexts = []

# connect to chal nc w pwntools
i = 0
conn = remote('lac.tf', 31140)
conn.recvline()
f1 = conn.recvline().decode('utf-8').strip()
f2 = conn.recvline().decode('utf-8').strip()

# send plaintexts and receive ciphertexts
for i in range(0, 20, 2):
    conn.recv()
    conn.sendline((plaintexts[i]+plaintexts[i+1]).encode('utf-8'))
    conn.recvline()
    ciphertexts.append(conn.recvline().decode('utf-8').strip())
    ciphertexts.append(conn.recvline().decode('utf-8').strip())

# get pt and ct matrices
ct_matrix = np.zeros([n, n])
for i in range(n):
    ct_matrix[i] = stov(ciphertexts[i])

pt_matrix = pt_matrix.T
ct_matrix = ct_matrix.T

# solve for A using sympy inv_mod
A = Matrix(ct_matrix) * Matrix(pt_matrix).inv_mod(95) % 95
A = np.array(A).astype(int)

conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
fakeflag2 = conn.recvline().decode('utf-8').strip()
conn.recvline()

# send encrypted first half
conn.recv()
first_half = encrypt(A, fakeflag2[:n])
conn.sendline(first_half.encode('utf-8'))

conn.recvline()

#send encrypted second half
conn.recv()
second_half = encrypt(A, fakeflag2[n:])
conn.sendline(second_half.encode('utf-8'))

conn.interactive()