


`self.layers=[(grid0,ents0),(grid1,ents1),...]`

`self.layers[$LID][0] = {(x,y):{tile_dict}}`

`self.layers[$LID][1] = {(x,y):entity_object}`

`tile_dict = {'tid':'???','dat':$numbers}`

`self.addlayer(grid=???,ents=???)`

`self.get_xy(x,y)` return slice of self.layers for just that xy coord

`self.find_entity(ent)` return x,y,layer of entity object (only one entity obj per map for all layers)

`self.draw(screen,locobj)` draws pre-rendered grid layers, then entities (g0,e0,g1,e1...)