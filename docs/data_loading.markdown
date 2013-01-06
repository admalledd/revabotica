data is saved as json. see relevant examples and other docs for what info is stored where. this talks about how it is all saved, where, and why.



root directory layout:

```
|-- assets
|   |-- img
|   |   |-- robots
|   |   `-- tiles
|   |-- music
|   `-- sfx
|-- saves
    `-- $savename
        |-- assets
        |   |-- img
        |   |   |-- robots
        |   |   `-- tiles
        |   |-- music
        |   `-- sfx
        |-- config.json
        |-- entities
        |   |-- 0.ejson
        |   `-- entities.json
        |-- grid
        |   `-- 0.grid
        `-- robots
            |-- 0
            |   `-- (0,0).json
            `-- robots.json
```


note that sometimes special care is needed to merge the different files, so we have the loaders.py take care of loading, merging, then returning the data. in the end of the load, the data should be a single python dictionary. (no support for returning lists, however we can load them and pass of parsing INTO a dict with special cased loaders. see loaders.py/load_grid()), saving is taken care of via savers.py, Note that loaders and savers will hopefully merge later into a better layout of code. get things working first though.

ok, now onto loading assets: these are basically any file that is not in JSON format / does not need merging with other files. so what happens here is that we use a `fs.multifs` that is loaded in the `rootfs/assets`,`saves/$savename/assets/` order, then merged into the single directory for the rootfs `fs.mountfs` as the `assets` directory.

Note for loading / saving of entities: due the fact that entities can move about, each entity must have a 100% unique $EID. This $EID is a json string in the .ejson files. (random generation?).