from pwn import *

'''
What is the 1th magic word? a
WRONG WORD! the word was knife
Goodbye...
'''

# store an array of magic words
# send each magic word to the server
# if the word is correct, then send the next word
# if the word is incorrect, then add the correct word to the array, close the connection, and start over
# if we reach the flag, then print the flag and exit

# connect to the server
conn = remote('chal.sigpwny.com', 5050)

# store the magic words
magic_words = []
 
# loop until we get the flag
while True:
    for word in magic_words:
        conn.recvuntil(b'magic word? ')
        conn.sendline(word)
    
    line = conn.recv()
    print(line)
    
    conn.sendline('a')
    line = conn.recvline()
    
    magic_words.append(line.split(b'word was ')[1].strip())
    print(magic_words)
    conn.close()
    
    conn = remote('chal.sigpwny.com', 5050)
    
    

