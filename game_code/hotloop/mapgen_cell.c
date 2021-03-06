#include <stdlib.h>
#include <time.h>

#include "utils.h"

#define TILE_FLOOR 46
#define TILE_WALL 35

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

int randpick(generation_params* params)
{
    if(rand()%100 < params->fillprob){
        return TILE_WALL;
    }
    else{
        return TILE_FLOOR;
    }
}

void initmap(generation_params* params)
{
    srand(time(NULL));
    (*py_logger)("Init map called");
    (*log_ints)("x:%d y:%d p:%d h:%d l:%d r:%d",6,params->size_x,params->size_y,params->fillprob,
           params->r1_cutoff,params->r2_cutoff,params->reps);
    int xi, yi;
    params->grid  = (int**)malloc(sizeof(int*) * params->size_y);
    params->grid2 = (int**)malloc(sizeof(int*) * params->size_y);

    for(yi=0; yi<params->size_y; yi++)
    {
        params->grid [yi] = (int*)malloc(sizeof(int) * params->size_x);
        params->grid2[yi] = (int*)malloc(sizeof(int) * params->size_x);
    }
    (*log_ints)("grid size:%d bytes",1,2*sizeof(int)*params->size_x*params->size_y);
    for(yi=1; yi<params->size_y-1; yi++)
        for(xi=1; xi<params->size_x-1; xi++)
            params->grid[yi][xi] = randpick(params);

    for(yi=0; yi<params->size_y; yi++)
        for(xi=0; xi<params->size_x; xi++)
            params->grid2[yi][xi] = TILE_WALL;

    for(yi=0; yi<params->size_y; yi++)
        params->grid[yi][0] = params->grid[yi][params->size_x-1] = TILE_WALL;
    for(xi=0; xi<params->size_x; xi++)
        params->grid[0][xi] = params->grid[params->size_y-1][xi] = TILE_WALL;
}

void delmap(generation_params* params)
{
    int yi=0;
    for (yi=0; yi<params->size_y;yi++)
    {
        free(params->grid[yi]);
        free(params->grid2[yi]);
    }
    free(params->grid);
    free(params->grid2);
}

void generation(generation_params* params)
{
    int xi, yi, ii, jj;

    for(yi=1; yi<params->size_y-1; yi++)
        for(xi=1; xi<params->size_x-1; xi++)
        {
            int adjcount_r1 = 0,
                              adjcount_r2 = 0;

            for(ii=-1; ii<=1; ii++)
                for(jj=-1; jj<=1; jj++)
                {
                    if(params->grid[yi+ii][xi+jj] != TILE_FLOOR)
                        adjcount_r1++;
                }
            for(ii=yi-2; ii<=yi+2; ii++)
                for(jj=xi-2; jj<=xi+2; jj++)
                {
                    if(abs(ii-yi)==2 && abs(jj-xi)==2)
                        continue;
                    if(ii<0 || jj<0 || ii>=params->size_y || jj>=params->size_x)
                        continue;
                    if(params->grid[ii][jj] != TILE_FLOOR)
                        adjcount_r2++;
                }
            if(adjcount_r1 >= params->r1_cutoff || adjcount_r2 <= params->r2_cutoff)
                params->grid2[yi][xi] = TILE_WALL;
            else
                params->grid2[yi][xi] = TILE_FLOOR;
        }
    for(yi=1; yi<params->size_y-1; yi++)
        for(xi=1; xi<params->size_x-1; xi++)
            params->grid[yi][xi] = params->grid2[yi][xi];
}
