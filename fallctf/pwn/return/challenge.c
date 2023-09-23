#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

// Ignore this function. It is just used to make
// the challenge work over the network.
void setup() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

// Call this function to win!
void print_flag() {
    // This bypasses some recent security features in glibc to simply your exploit.
    __asm__("sub $0x8, %rsp");
    system("/bin/cat ./flag.txt");
}

int main() {
    char name[32];

    setup();

    puts("Hey, what's your name?");

    // Overflow the buffer and write the address of print_flag to the return
    // address of main!
    // Get the address of print_flag using gdb! (It's always the same)
    gets(name);
    printf("Nice to meet you, %s.\n", name);

    return 0;
}
