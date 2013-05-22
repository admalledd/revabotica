import time

import random
try:
    import cStringIO as sio
except ImportError:
    print "using slower stringIO"
    import StringIO as sio
import sys
TILE_FLOOR=0
TILE_WALL=1



class generation_params:
    def __init__(self):
        '''typedef struct {
                int r1_cutoff, r2_cutoff;
                int reps;
            } generation_params; '''
        self.r1_cutoff = 0
        self.r2_cutoff = 0
        self.reps = 0

class cell_grid(object):
    def __init__(self):
        self.grid  = []
        self.grid2 = []
 
        self.fillprob = 40

        self.r1_cutoff = 5
        self.r2_cutoff = 2

        self.size_x = 64
        self.size_y = 20

        self.params = generation_params()

        self.params_set = []

    def randpick(self):
        if(random.randint(1,100) < self.fillprob):
            return TILE_WALL
        else:
            return TILE_FLOOR


    def initmap(self):
        
        self.grid  = range(self.size_y)
        self.grid2 = range(self.size_y)
    
        for yi in range(self.size_y):
            self.grid[yi]  = range(self.size_x)
            self.grid2[yi] = range(self.size_x)
    
    
        for yi in range(1,self.size_y-1):
            for xi in range(1,self.size_x-1):
                self.grid[yi][xi] = self.randpick()
    
        for yi in range(0,self.size_y):
            for xi in range(0,self.size_x):
                self.grid2[yi][xi] = TILE_WALL
    
        for yi in range(self.size_y):
            self.grid[yi][0] = self.grid[yi][self.size_x-1] = TILE_WALL
        for xi in range(1,self.size_x-1):
            self.grid[0][xi] = self.grid[self.size_y-1][xi] = TILE_WALL


    def generation(self):
        
        for yi in range(1,self.size_y-1):
            for xi in range(1,self.size_x-1):
                adjcount_r1 = 0
                adjcount_r2 = 0
            
                for ii in range(-1,2,1):
                    for jj in range(-1,2,1):
                        if self.grid[yi+ii][xi+jj] != TILE_FLOOR:
                            adjcount_r1 += 1 #if surrounding tiles are not floor
            
                for ii in range(yi-2,yi+3):
                    for jj in range(xi-2,xi+3):
                        if(abs(ii-yi)==2 and abs(jj-xi)==2):
                            continue
                        if(ii<0 or jj<0 or ii>=self.size_y or jj>=self.size_x):
                            continue #edge of map
                        if(self.grid[ii][jj] != TILE_FLOOR):
                            adjcount_r2+=1 #if we are mostly surrounded by floor
            
                if adjcount_r1 >  self.params.r1_cutoff or adjcount_r2 < self.params.r2_cutoff :
                    self.grid2[yi][xi] = TILE_WALL
                else:
                    self.grid2[yi][xi] = TILE_FLOOR
        
        for yi in range(1,self.size_y-1):
            for xi in range(1,self.size_x-1):
                self.grid[yi][xi] = self.grid2[yi][xi]

    def printfunc(self,generations):
    
        print "W[0](p) = rand[0,100) < %i"%self.fillprob
    
        for ii in range(generations):
    
            sys.stdout.write("Repeat %i: W'(p) = R[1](p) >= %i"%(self.params_set[ii].reps, self.params_set[ii].r1_cutoff))
        
            if self.params_set[ii].r2_cutoff >= 0 :
                sys.stdout.write(" || R[2](p) <= %i\n"%(self.params_set[ii].r2_cutoff))
            else:
                sys.stdout.write('\n')
    


    def printmap(self):
    
        for yi in range(self.size_y):
            for xi in range(self.size_x):
                    if self.grid[yi][xi] == TILE_WALL:
                        sys.stdout.write('#')
                    else:
                        sys.stdout.write('.')
            
            sys.stdout.write('\n')
    def get_map(self):
        s = sio.StringIO()
        for yi in range(self.size_y):
            for xi in range(self.size_x):
                    if self.grid[yi][xi] == TILE_WALL:
                        s.write('#')
                    else:
                        s.write('.')
            
            s.write('\n')
        return s.getvalue()
    

    def main(self,argv):
        argv = argv.split()
        
        self.size_x     = int(argv[1])
        
        self.size_y     = int(argv[2])
        
        self.fillprob   = int(argv[3])
        
        
        generations = (len(argv)-4)/3
        
        
        self.params_set=[]
        
        for ii in range(4,len(argv)-2,3):
            self.params=generation_params()
            self.params.r1_cutoff  = int(argv[ii])
            self.params.r2_cutoff  = int(argv[ii+1])
            self.params.reps = int(argv[ii+2])
            self.params_set.append(self.params)
        
        self.initmap()
        
        for ii in range(generations):
            self.params = self.params_set[ii]
            for jj in range(self.params.reps):
                open('tests/test.map.%s'%jj,'w').write(self.get_map())
                self.generation()
                print 'generation:(%s,%s)'%(ii,jj)
        self.printfunc(generations)
        #self.printmap()
        return 0

if __name__ == '__main__':
    g=cell_grid()
    #g.main("test 120 64 50 8 8 25")
    g.main("test 640 640 40 8 7 25")
    #g.printmap()
    open('test.map','w').write(g.get_map())