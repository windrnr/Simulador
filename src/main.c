#define SIMLIB_IMPLEMENTATION
#include "simlib.h"

int main(int argc, char **argv) {
        if (argc != 2) {
                fprintf(stderr, "El uso es '%s' <path>.\n", argv[0]);
                exit(EXIT_FAILURE);
        }

        if (*argv[1] == '\0') {
                fprintf(stderr, "Una dirección no ha sido provista\n");
                exit(EXIT_FAILURE);
        }

        Parse_csv(argv[1], 2);
        return 0;
}



