#ifndef SIMU_H_
#define SIMU_H_
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

void Parse_csv(const char *filepath, int column_num);

#endif // SIMU_H_

#ifdef SIMU_IMPLEMENTATION

char* get_campo(char* line, int num){
        char* token; 
        for(token = strtok(line, ";"); token && *token; token = strtok(NULL, ";")){
                if (num == 0){
                        return token;
                }
                num -= 1;
        }
        return NULL;
}

char* readContent(const char *path) {
        FILE *file_ptr = fopen(path, "r");
        if (file_ptr == NULL) {
                fprintf(stderr, "[%s] Error abriendo '%s': %s\n", __func__, path, strerror(errno));
                exit(EXIT_FAILURE);
        }

        fseek(file_ptr, 0, SEEK_END);
        size_t file_size = ftell(file_ptr);
        rewind(file_ptr);

        char *content = (char *)malloc(file_size + 1);

        if (content == NULL) {
                fclose(file_ptr);
                fprintf(stderr, "[%s] Error asignando memoria para almacenar el contenido del archivo: %s.\n", __func__, strerror(errno));
                exit(EXIT_FAILURE);
        }

        size_t bytes_read = fread(content, 1, file_size, file_ptr);
        content[bytes_read] = '\0';

        if (bytes_read != file_size) {
                free(content);
                fclose(file_ptr);
                fprintf(stderr, "[%s] Error leyendo el archivo: %s.\n", __func__, strerror(errno));
                exit(EXIT_FAILURE);
        }
        fclose(file_ptr);
        return content;
}

void Parse_csv(const char *filepath, int column_num) {
        char* content = readContent(filepath);
        char* line_ptr = (char*)strtok(content, "\n");
        while (line_ptr != NULL) {
                printf("DEBUG 2 BEFORE: %s \n", line_ptr);
                char* result = get_campo(line_ptr, column_num);
                printf("El dato en la columna %d es: %s\n", column_num, result);
                line_ptr = strtok(NULL, "\n");
                printf("DEBUG 2 AFTER: %s\n", line_ptr);
        }
        free(content);
}

#endif // SIMU_IMPLEMENTATION
