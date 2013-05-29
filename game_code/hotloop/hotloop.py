from cffi import FFI
ffi=FFI()

ffi.cdef('''

int rawint;

int SampleAddInt(int i1, int i2);

void SampleFunction1();

int SampleFunction2();


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

lib.SampleFunction1()

def mapgen_cell(size_x,size_y,fillprob,r1_cutoff,r2_cutoff,reps):
    '''Generate a cell map, then return the final string of the map'''
    def get_map(params):
        '''helper to convert map to string'''
        grid_out=[]
        for y in range(params.size_y):
            grid_out.append([])
            for x in range(params.size_x):
                if params.grid[y][x] == 1:
                    grid_out[y].append('#')
                elif params.grid[y][x] == 0:
                    grid_out[y].append('.')
            grid_out[y]=''.join(grid_out[y])
        #grid_out.insert(0,str(lib.szof(params)))
        return '\n'.join(grid_out)

    parms = ffi.new('generation_params *')
    parms.r1_cutoff=r1_cutoff
    parms.r2_cutoff=r2_cutoff
    parms.fillprob = fillprob
    parms.size_y = size_y
    parms.size_x = size_x
    parms.reps =reps

    lib.initmap(parms)
    for jj in range(reps):
        with open('tests/test.map.%05d'%jj,'w') as f:
            f.write(get_map(parms))
        print 'generation:(%s)'%(jj)
        lib.generation(parms)
    
    open('tests/test.map.%s'%(jj+1),'w').write(get_map(parms))
    out = get_map(parms)
    lib.delmap(parms)
    
    del parms
    return out
if __name__ == '__main__':
    mapgen_cell(120,120,80,8,8,2500)