the grid format is json, with two major ways to store the data: 

1. sparse, where each entry has a x,y data point as well.

2. full grid, loaded in order of `[[row],[row],[row]]`

see `test1.map/grid/0.grid` for a small example of a "full grid", and `test1.map/grid/1.grid` for "sparse".

It is recomended that 0.grid be a full grid for ease of use reasons considering its the background layer

files are named in the convention of `grid/$GRID_LAYER_ID.grid` which is from 0 up. abbreviated GID.

load order is `/default/maps/$mapname/grid/$GID.grid` then `/local/maps/$mapname/grid/$GID.grid`