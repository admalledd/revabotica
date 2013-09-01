
#include "utils.h"


#include <stdarg.h>
#include <alloca.h>

void log_ints(char* message, int how_many, ...) {
    va_list ap;
    /* collect the "..." arguments into the values[] array */
    int i, *values = alloca(how_many * sizeof(int));
    va_start(ap, how_many);
    for (i=0; i<how_many; i++)
        values[i] = va_arg(ap, int);
    va_end(ap);

    (*py_logger_ints)(message, how_many, values);
}

