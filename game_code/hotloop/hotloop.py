import struct

from cffi import FFI
ffi=FFI()

ffi.cdef('''

int rawint;

int SampleAddInt(int i1, int i2);

void SampleFunction1();

int SampleFunction2();

//utils.c/h
void (*py_logger)(char *);
void (*py_logger_ints)(char * message, int how_many, int * values);


//mapgen_cell.c
typedef struct
{
    int r1_cutoff, r2_cutoff;
    int reps;
    int fillprob;
    int size_x;
    int size_y;
    int **grid;
    int **grid2;
} generation_params;

int randpick(generation_params* params);
void initmap(generation_params* params);
void generation(generation_params *params);
void delmap(generation_params *params);
    ''')
lib = ffi.dlopen('./libhotloop.so')
@ffi.callback("void(char *)")
def logger(message):
    print "::hotloop.so::"+ffi.string(message)
@ffi.callback("void(char *,int, int *)")
def logger_ints(message,num_args,args):
    f=[]
    for i in range(num_args):
        f.append(int(args[i]))
    print "::hotloop.so::"+ffi.string(message)%tuple(f)

lib.py_logger = logger
lib.py_logger_ints = logger_ints
lib.SampleFunction1()

def mapgen_cell(size_x,size_y,fillprob,r1_cutoff,r2_cutoff,reps):
    '''Generate a cell map, then return the final string of the map'''
    def get_map(params):
        '''helper to convert map to string'''
        #return "nope.jpg"
        grid_out=[]
        for y in xrange(params.size_y):
            #st = struct.pack('i'*params.size_x,*(params.grid[y][x] for x in xrange(params.size_x)))

            grid_out.append(''.join((chr(params.grid[y][x]) for x in xrange(params.size_x))))
        return '\n'.join(grid_out)

    parms = ffi.new('generation_params *')
    parms.r1_cutoff=r1_cutoff
    parms.r2_cutoff=r2_cutoff
    parms.fillprob = fillprob
    parms.size_y   = size_y
    parms.size_x   = size_x
    parms.reps     = reps
    print parms.grid
    lib.initmap(parms)
    for jj in range(reps):
        with open('tests/test.map.%05d'%jj,'wb') as f:
            f.write(get_map(parms))
        #print 'generation:(%s)'%(jj)
        lib.generation(parms)
    
    open('tests/test.map.%s'%(jj+1),'w').write(get_map(parms))
    out = get_map(parms)
    print parms.grid
    #import pdb; pdb.set_trace()
    lib.delmap(parms)
    # print "freed old grid, forcing write"
    # parms.grid[0][0]=12
    # print "forcing read"
    # print parms.grid[0][0]
    # print "getting cffi data on grid"
    # print parms.grid
    del parms
    return out
class cell_gen(object):
    def __init__(self,size_x,size_y,fillprob=50,r1_cutoff=8,r2_cutoff=8,generations=25):
        #set parameters to cell generation stuff
        self.parms = ffi.new('generation_params *')
        self.parms.r1_cutoff=r1_cutoff
        self.parms.r2_cutoff=r2_cutoff
        self.parms.fillprob = fillprob
        self.parms.size_y   = size_y
        self.parms.size_x   = size_x
        self.parms.reps     = generations

        #allocate memory, do random seeding based on fillprob
        lib.initmap(self.parms)
    def __del__(self):
        lib.delmap(self.parms)
        del self.parms
    def generate_map(self,debug=False):
        pass

if __name__ == '__main__':
    final_map = mapgen_cell(80,80,80,8,8,2)
    with open('test.map','wb') as bleh:
        bleh.write(final_map)
    #mapgen_cell(1000,50000,80,8,8,2)