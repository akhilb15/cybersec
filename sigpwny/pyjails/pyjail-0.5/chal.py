#!/usr/bin/env python3

#Flag is at /flag.txt

def is_bad(user_input):
    # Ok guys my last system was nuked... now you can only eval
    return 'flag' in user_input


def main():

    print("You wake up in a jail lounge with handcuffs on. Your head is still sore from the bonk.")

    user_input = input('You only have enough energy to mutter one sentence. What do you have to say for yourself? ')

    if is_bad(user_input):
        print('Sorry, not good enough. Go back to jail.')
        return
    
    try:
        eval(user_input)
        print("Ok, we'll consider it.")
    except:
        print('Sorry, not good enough. Go back to jail.')


if __name__ == '__main__':
    main()
