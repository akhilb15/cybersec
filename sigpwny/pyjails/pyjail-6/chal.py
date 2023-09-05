#!/usr/bin/env python3

#Flag is at /flag.txt

from RestrictedPython import compile_restricted
from RestrictedPython import Eval
from RestrictedPython import Guards
from RestrictedPython import safe_globals
from RestrictedPython import utility_builtins
from RestrictedPython.PrintCollector import PrintCollector

def exec_super_ultra_high_maximum_security_jail(code):
    """Interprets the given python code inside a safe execution environment"""

    def safe_import(name, *args, **kwargs):
        whitelist = ['math', 'json', 'string', 're',
                     'random', 'datetime', 'itertools', 'time', 'requests']
        if name in whitelist:
            return __import__(name, *args, **kwargs)
        raise ImportError(
            f'Bonk no import for you!!!')
    code += "\nresults = printed"
    byte_code = compile_restricted(
        code,
        filename="<string>",
        mode="exec",
    )
    policy_globals = {**safe_globals, **utility_builtins}
    policy_globals['__builtins__']['__metaclass__'] = type
    policy_globals['__builtins__']['__name__'] = type
    policy_globals['__builtins__']['__import__'] = safe_import
    policy_globals['_getattr_'] = Guards.safer_getattr
    policy_globals['_getiter_'] = Eval.default_guarded_getiter
    policy_globals['_getitem_'] = Eval.default_guarded_getitem
    policy_globals['_write_'] = Guards.full_write_guard
    policy_globals['_print_'] = PrintCollector
    policy_globals['_iter_unpack_sequence_'] = Guards.guarded_iter_unpack_sequence
    policy_globals['_unpack_sequence_'] = Guards.guarded_unpack_sequence
    policy_globals['enumerate'] = enumerate
    exec(byte_code, policy_globals, None)
    return policy_globals["results"]


def main():

    print("You wake up in a maximum security jail cell with guards surrounding you.")

    user_input = input('What do you have to say for yourself? ')

    print(exec_super_ultra_high_maximum_security_jail(user_input))

if __name__ == '__main__':
    main()