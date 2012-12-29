data is saved as json. see relevent examples and other docs for what info is stored where. this talks about how it is all saved, where, and why.

there is a basic idea: load multiple json sources and merge them together. the different sources are under the pyfsobj under these names and are loaded in this order:

1. `default` everything in this directory is read only, has all the default files/maps/assest ect...

2. `local` is any pyfs open-able URL, so see [the pyfs opendir docs.](http://packages.python.org/fs/opener.html#module-fs.opener), this is so that players can load their own maps from any compatible location (eg, load from URL)

3. `saves` this is where all the writes go.


directory layout:

```
|-- assets
|   |-- img
|   |   |-- robots
|   |   `-- tiles
|   |-- music
|   `-- sfx
|-- maps
    `-- $mapname
        |-- assets
        |   |-- img
        |   |   |-- robots
        |   |   `-- tiles
        |   |-- music
        |   `-- sfx
        |-- config.json
        |-- entities
        |   |-- 0
        |   |   `-- (0,0).json
        |   `-- entities.json
        |-- grid
        |   |-- 0.grid
        |   `-- 0.py
        `-- robots
            |-- 0
            |   `-- (0,0).json
            `-- robots.json
```

`saves` / `local` have the same layout, but remember that the `default` dir MUST have everything needed to play. 

`saves` is slightly diffrent in that there are multiple saves, so the strucutre above is in each save folder. eg: `default/maps/$mapname/config.json` == `local/maps/$mapname/config.json` == `saves/$savename/maps/$mapname/config.json`


note that sometimes special care is needed to merge the different files, so we have the loaders.py take care of loading, merging, then returning the data. in the end of the load, the data should be a single python dictionary. (no support for returning lists, however we can load them and pass of parsing INTO a dict with special cased loaders. see loaders.py/load_grid())


ok, now onto loading assets: these are basically any file that is not in JSON format / does not need merging with other files. so what happens here is that we use a `fs.multifs` that is loaded in the same order as above, then merged into the single `fs.mountfs` as the `assets` directory.