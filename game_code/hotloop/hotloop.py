from cffi import FFI
ffi=FFI()

ffi.cdef('''

int rawint;

int SampleAddInt(int i1, int i2);

void SampleFunction1();

int SampleFunction2();


//mapgen_cell.c

#define TILE_FLOOR ...
#define TILE_WALL ...

typedef struct {
    int r1_cutoff, r2_cutoff;
    int reps;
} generation_params;

int **grid;
int **grid2;

int fillprob = 40;
int size_x = 64, size_y = 20;
generation_params *params;

generation_params *params_set;
int generations;

int randpick(void);
void initmap(void);
void generation(void);
void delmap(void);

    ''')
lib = ffi.dlopen('./libhotloop.so')

lib.SampleFunction1()

def mapgen_cell(size_x,size_y,fillprob,r1_cutoff,r2_cutoff,reps):
    '''Generate a cell map, then return the final string of the map'''
    def get_map():
        '''helper to convert map to string'''
        grid_out=[]
        for y in range(lib.size_y):
            grid_out.append([])
            for x in range(lib.size_x):
                if lib.grid[y][x] == 1:
                    grid_out[y].append('#')
                elif lib.grid[y][x] == 0:
                    grid_out[y].append('.')
            grid_out[y]=''.join(grid_out[y])
        return '\n'.join(grid_out)

    lib.size_x = size_x
    lib.size_y = size_y
    parms = ffi.new('generation_params *')
    parms.r1_cutoff=r1_cutoff
    parms.r2_cutoff=r2_cutoff
    parms.reps =reps
    lib.params = parms
    lib.initmap()
    
    for jj in range(reps):
        open('tests/test.map.%s'%jj,'w').write(get_map())
        print 'generation:(%s)'%(jj)
        lib.generation()
    
    open('tests/test.map.%s'%(jj+1),'w').write(get_map())
    out = get_map()
    lib.delmap()
    del parms
    return out
if __name__ == '__main__':
    print mapgen_cell(64,64,50,8,8,25)