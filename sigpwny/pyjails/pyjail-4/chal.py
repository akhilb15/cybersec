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
        'cat'
        'flag',
        'txt',
        '"',
        '+'
    ]
    for bad in blacklist:
        if bad in user_input:
            return True
    return False


def main():

    print("You wake up back in a jail cell. Your ears are ringing, and you can't hear anything. ")

    user_input = input('What do you have to say for yourself? ')

    if is_bad(user_input):
        print('Sorry, not good enough. Go back to jail.')
        return
    
    try:
        exec(user_input)
    except Exception:
        print('Sorry, not good enough. Go back to jail.')


if __name__ == '__main__':
    main()
