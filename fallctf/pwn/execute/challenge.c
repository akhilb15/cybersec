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

int main() {
    char name[32];

    setup();

    printf("Hey, what's your darkest secret? I'm keeping it at %p\n", &name);

    // You can still overflow the buffer and set a return address...
    // But there's no win function. Luckily, the stack is executable!
    gets(name);
    puts("Wow, what a tale!");

    return 0;
}
