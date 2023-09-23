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

int vuln(){
    char name[32];
    char place[32];
    printf("Hey, what's your name?\n");
    fgets(name, 64, stdin);
    printf("Hello, ");
    printf(name);

    printf("Where are you from?\n");
    fgets(place, 64, stdin);

}

int main() {
    setup();
    vuln();
    return 0;
}
