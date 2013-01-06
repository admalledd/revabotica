
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


required methods:

* `self.update(mapobj)` update entity (if needed, most scrap will be no-ops here for example). it is recomended that you use a `pyglet.clock.Clock()` and schedule events based on time with the [schedule_interval](http://www.pyglet.org/doc/api/pyglet.clock-module.html#schedule_interval)

* `self.draw(px,py)` draw onto the screen at location px and py. (check if pyglet.graphics.Batch would work here?)

* `self.load_data(data)` parses the dictionary `data` into at least the required attributes listed below.

required attributes:

* `self.img` 2d texture of the entity, can have transparencies. for animations just change this every frame.

* `self.lang` a dictionary of all strings that are displayed to the user ever. eg, name, flavor text, anything. this is so that changing languages should be easier.
