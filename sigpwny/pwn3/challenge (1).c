#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void setup() {
    // you can ignore this stuff. it's just for netcat to place nice
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

int main() {
    char answer[32];
    
    setup();

    puts("Hello, what is your name?");
    gets(answer);
    puts("Nice to meet you!");

    return 0;
}