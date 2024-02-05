
def xor(a, b):
    return b''.join([(x ^ y).to_bytes(1,'big') for (x,y) in zip(a,b)])

ciphertexts = open("message.txt", "r").read().strip("[] ").split(',')

n = len(ciphertexts)
for i in range(n):
    ciphertexts[i] = bytes.fromhex(ciphertexts[i].strip("' ")) # get rid of extra apostrophes and whitespace, then convert hex string to bytes

# basic idea: ciphertext1 ^ ciphertext2 = plaintext1 ^ plaintext2 => (ciphertext1 ^ ciphertext2) ^ plaintext2 = plaintext1
# we know the start of one of the plain texts is 'sigpwny{' and we know all the ciphertexts -> crib dragging
# step 1: xor the flag string (the last one in the array) with all the other ciphertexts one at a time, each time xoring the result with 'sigpwny{' 
# step 2: step 1 will give the first 8 characters (length of 'sigpwny{') of all the plaintexts, from there we choose one of those where we can guess
# the rest of the word and then replace 'sigpwny{' with the entire beginning of the plaintext you chose
# step 3: keep this process going, alternating between guessin plaintexts and filling in the flag until the entire flag shows up
# -> will make more sense looking at the process below

# this is kinda trial and error btw

for i in range(n-1):
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'sigpwny')) -> 'Crib dr' showed up so I guessed Crib dragging
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'Crib dragging')) -> 'sigpwny{they_' showed up so I filled that in for the flag
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'sigpwny{they_')) -> 'Modern crypto'
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'Modern cryptography')) -> 'sigpwny{they_rebo'e' -> looks like reboot
    # --> the one above looks messed up bc theres actually a random space in the pt lol ('Modern cryptograp hy')
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'sigpwny{they_reboot')) -> 'The growth  of cryp' -> extra space not typo 
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'The growth  of cryptography')) -> 'sigpwny{they_rebooted_mtv_s' 
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'sigpwny{they_rebooted_mtv_s')) -> 'Crib dragging is a known p|' 
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'Crib dragging is a known plaintext attack')) -> "sigpwny{they_rebooted_mtv_crib'Ntb\x0bs%2$\x7f" 
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'sigpwny{they_rebooted_mtv_crib')) -> 'There are two types of cryptog'
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'There are two types of cryptography')) -> 'sigpwny{they_rebooted_mtv_cribs_in_'
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'sigpwny{they_rebooted_mtv_cribs_in_')) -> 'Crib dragging is a known plain text'
    print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'Crib dragging is a known plain text attack')) # -> sigpwny{they_rebooted_mtv_cribs_in_2021} <- THE FLAG
    # print(xor(xor(ciphertexts[n-1], ciphertexts[i]), b'sigpwny{they_rebooted_mtv_cribs_in_2021}'))



