#!/usr/bin/env python3

#Flag is at /flag.txt

def is_bad(user_input):
    blacklist = [
        'import',
        'eval',
        'exec',
        'system',
        'compile',
        'os',
        'chr',
        'input',
        'open',
        'cat',
        'lower'
    ]
    blacklist += [
        'L',
        '+',
        'ratio',
        '+',
        'flag',
        '.',
        'txt',
        '!',
        '@',
        '#',
        '$',
        '%',
        '^',
        '&',
        '*',
        '[', 
        ']',
        '_',
        '+',
        '"',
        ':',
    ]
    for bad in blacklist:
        if bad.lower() in user_input.lower():
            return True
    return False


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
