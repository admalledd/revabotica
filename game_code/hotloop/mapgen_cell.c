 #include <stdio.h>
 #include <stdlib.h>
 #include <time.h>

 #define TILE_FLOOR 0
 #define TILE_WALL 1

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
 int generations=0;

 int randpick(void)
 {
    if(rand()%100 < fillprob)
        return TILE_WALL;
    else
        return TILE_FLOOR;
 }

 void initmap()
 {
    srand(time(NULL));
    int xi, yi;

    grid  = (int**)malloc(sizeof(int*) * size_y);
    grid2 = (int**)malloc(sizeof(int*) * size_y);

    for(yi=0; yi<size_y; yi++)
    {
        grid [yi] = (int*)malloc(sizeof(int) * size_x);
        grid2[yi] = (int*)malloc(sizeof(int) * size_x);
    }

    for(yi=1; yi<size_y-1; yi++)
    for(xi=1; xi<size_x-1; xi++)
        grid[yi][xi] = randpick();

    for(yi=0; yi<size_y; yi++)
    for(xi=0; xi<size_x; xi++)
        grid2[yi][xi] = TILE_WALL;

    for(yi=0; yi<size_y; yi++)
        grid[yi][0] = grid[yi][size_x-1] = TILE_WALL;
    for(xi=0; xi<size_x; xi++)
        grid[0][xi] = grid[size_y-1][xi] = TILE_WALL;
 }

 void delmap(void){
    free(grid);
    free(grid2);
 }

 void generation(void)
 {
    int xi, yi, ii, jj;

    for(yi=1; yi<size_y-1; yi++)
    for(xi=1; xi<size_x-1; xi++)
    {
        int adjcount_r1 = 0,
            adjcount_r2 = 0;

        for(ii=-1; ii<=1; ii++)
        for(jj=-1; jj<=1; jj++)
        {
            if(grid[yi+ii][xi+jj] != TILE_FLOOR)
                adjcount_r1++;
        }
        for(ii=yi-2; ii<=yi+2; ii++)
        for(jj=xi-2; jj<=xi+2; jj++)
        {
            if(abs(ii-yi)==2 && abs(jj-xi)==2)
                continue;
            if(ii<0 || jj<0 || ii>=size_y || jj>=size_x)
                continue;
            if(grid[ii][jj] != TILE_FLOOR)
                adjcount_r2++;
        }
        if(adjcount_r1 >= params->r1_cutoff || adjcount_r2 <= params->r2_cutoff)
            grid2[yi][xi] = TILE_WALL;
        else
            grid2[yi][xi] = TILE_FLOOR;
    }
    for(yi=1; yi<size_y-1; yi++)
    for(xi=1; xi<size_x-1; xi++)
        grid[yi][xi] = grid2[yi][xi];
 }
