#ifndef SIMLIB_H_
#define SIMLIB_H_
#define COLOR_BOLD "\033[1m"
#define COLOR_OFF "\033[m"
#define COLOR_RED 31
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

void Parse_csv(const char *filepath, int column_num);

#endif // SIMLIB_H_

#ifdef SIMLIB_IMPLEMENTATION

char* get_campo(char* line, int num){
        char* token; 
        for(token = strtok(line, ";"); /*CONDICIONAL VACÍO*/ ; token = strtok(NULL, ";\n")){
                if (token == NULL)
                    return NULL;

                if (*token == '\0')
                    return NULL;

                if (num == 1)
                    return token;

                num -= 1;
        }
        return NULL;
}

void Parse_csv(const char *filepath, int column_num) {
        char* extension = strrchr(filepath, '.');
        if (extension != NULL && extension != filepath){
            if (strcmp(extension+1, "csv") != 0) {
                fprintf(stderr, "[%s] Error: Debe recibirse como entrada un archivo con extensión '.csv'.\n", __func__);
                exit(EXIT_FAILURE);
            }
        }

        FILE *file_ptr = fopen(filepath, "r");
        if (file_ptr == NULL) {
                fprintf(stderr, "[%s] Error: Ha ocurrido un error abriendo '%s': %s\n",__func__, filepath, strerror(errno));
                exit(EXIT_FAILURE);
        }

        char line[1024];
        while(fgets(line, 1024, file_ptr)) {
                char* line_ptr = strdup(line);
                printf("El campo %d es: %s\n", column_num, get_campo(line_ptr, column_num));
                free(line_ptr);
        }
}

#endif // SIMLIB_IMPLEMENTATION
