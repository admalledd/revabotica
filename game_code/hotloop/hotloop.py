from cffi import FFI
ffi=FFI()

ffi.cdef('''

int rawint;

int SampleAddInt(int i1, int i2);

void SampleFunction1();

int SampleFunction2();
    ''')
lib = ffi.dlopen('./libhotloop.so')

lib.SampleFunction1()

print lib.SampleFunction2()
import time;time.sleep(1)
print lib.SampleFunction2()
print lib.SampleFunction2()
print lib.SampleFunction2()
print lib.SampleFunction2()