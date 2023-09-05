#!/usr/bin/env python3

#Flag is at /flag.txt

import hashlib


def is_bad(user_input):
    #You can have at most 10 unique characters in your input!
    num_unique = len(set(user_input))
    return num_unique > 10


def main():

    print("You wake up in a jail cell. Your head is still sore from the bonk.")

    user_input = input('What do you have to say for yourself? ')

    if is_bad(user_input):
        print('Sorry, not good enough. Go back to jail.')
        return
    
    try:
        exec(user_input)
        print("Ok, we'll consider it.")
    except:
        print('Sorry, not good enough. Go back to jail.')


if __name__ == '__main__':
    main()
