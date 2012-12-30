file name is `entities/$layerid/(x,y).json`

```json

{
    "code_class":"part", //class to load and inject data into
    "data":{ //data to load with the entity's .load_data()
        "img":"img/entities/parts/scrap1.png", 
        "lang_file":"parts/scrap1.json",
        "amount":15
    }

}

```


`self.update(mapobj)` update entity (if needed, most scrap will be no-ops here for example). it is recomended that you use a `pyglet.clock.Clock()` and schedule events based on time with the [schedule_interval](http://www.pyglet.org/doc/api/pyglet.clock-module.html#schedule_interval)