#sys imports
#import pprint

#local imports
import lib.helpers
import loaders

class map(loaders.json_mixin,loaders.fs_load_mixin,loaders.grid_mixin):
    def __init__(self,fspath):
        self.layers=[]
        self.load_map(fspath)
     
    def add_layer(self,entity=None,tile=None):
        if entity == None and tile == None:
            raise Error("both cannot be none")
        #more magiks. self.layes must be iterable

    def load_map(self,fspath):
    	'''load a map. fspath is a pyfs compatible read only directory (see http://packages.python.org/fs/opener.html)'''
    	self.open_fspaths(fspath)

    	#load config files
    	self.settings=self.load_cfg('config.json')
        #print self.settings
        self.load_grid(0)

        #self.elayers=(layobj1,layobj2)#low to high
        #self.tlayers=(tobj1,tobj2)#low to high, last is top layer.
        ####len(self.elayers) == len(self.tlayers)
        #self.layers=magiks.dual_list(self.elayers,self.tlayers)
