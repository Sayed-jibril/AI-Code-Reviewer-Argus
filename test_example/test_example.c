#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAGIC_NUMBER 12345  // Magic number

char* api_key = "sk-1234567890abcdef"; // Hardcoded secret

void bad_function(char* input) {
    char buffer[100];
    
    // Buffer overflow risks
    strcpy(buffer, input);  // Dangerous strcpy
    strcat(buffer, "more"); // Dangerous strcat
    sprintf(buffer, "value: %s", input); // Dangerous sprintf
    
    // Memory management issues
    char* ptr = malloc(1000); // malloc without NULL check
    // Missing free(ptr)
    
    // Performance issues
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            for (int k = 0; k < 10; k++) {
                printf("%d, %d, %d\n", i, j, k);
            }
        }
    }
    
    // Quality issues
    if (MAGIC_NUMBER == 12345) {
        goto cleanup; // Avoid goto
    }
    
cleanup:
    return;
}

int main() {
    char* user_input = "test";
    bad_function(user_input);
    return 0;
}
