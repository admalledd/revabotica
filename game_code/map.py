#sys imports
import json
import sys
import logging
logger=logging.getLogger('map')

#package imports
import fs.path
import fs.errors

#local imports
import lib.helpers
import loaders

class map(object):
    def __init__(self,fspath):
        self.layers=[]
        self.load_map(fspath)
     
    def add_layer(self,entity=None,tile=None):
        if entity == None and tile == None:
            raise Error("both cannot be none")
        #more magiks. self.layes must be iterable

    def load_map(self,fspath):
    	'''load a map. fspath is a pyfs compatible read only directory (see http://packages.python.org/fs/opener.html)'''
    	self.fsobj = loaders.open_fspaths(fspath)

    	#load config files
    	self.settings=self.load_json('config.json')
        #print self.settings
        self.load_grid(0)

        #self.elayers=(layobj1,layobj2)#low to high
        #self.tlayers=(tobj1,tobj2)#low to high, last is top layer.
        ####len(self.elayers) == len(self.tlayers)
        #self.layers=magiks.dual_list(self.elayers,self.tlayers)
    def load_grid(self,gid):
        '''grid format: .grid file is a json file, see docs/grid_format.markdown for more info
           no overrides of the grid layout is allowed :C have to keep it the same for all layers to prevent overdraw.

        now, note that tile grids are always in pairs with entity layers,
            so this mixin actually also has the entity code
        
        there is ALWAYS a grid with GID==0 (the background)

        due to two diffrent ways that the tile info is actually stored (sparse vs full)
            initial load, detect, pass off to sub-helpers
            then update the grid with the data from the localdir (so load again really...)
        '''
        grid_path = fs.path.join('grid','%s.grid'%gid)
        default =self.load_json_default(grid_path)
        if type(default) == list:
            logger.info('loading default "%s.grid" as "full"'%gid)
            default=self.load_grid_full(default)


    def load_grid_full(self,gridlist):
        """load a grid based on a 2d list of dictionaries, see docs/grid_format.markdown for more info"""
        
        

    def load_json(self,name,autocreate=True):
        '''loads cfg in the order of: default, u#'s then "local"'''
        
        return self.merge_json(self.load_json_default(name),self.load_json_local(name,autocreate))

    def load_json_single(self,fspath,allow_fail=True):
        '''load one json file, checking if it exists, if it fails for some reason, return "None"'''
        try:
            return json.load(self.fsobj.open(fspath))
        except fs.errors.ResourceNotFoundError as e:
            if allow_fail:
                return None
            else:
                raise

    def load_json_default(self,name,allow_fail=False):
        '''loads default json file of $name'''
        default = self.load_json_single(fs.path.join('default',name),allow_fail)
        if allow_fail == True and default == None:
            logger.info('no default json file %s, ignoring'%name)
            default = {}
        return default

    def load_json_local(self,name,autocreate=True):
        
        local = self.load_json_single(fs.path.join('local',name))
        if autocreate and local == None:
            #could not open file, no local copy exists. create a blank one and use that
            logger.info('no local version of "%s", creating blank'%name)
            f=self.fsobj.open(fs.path.join('local',name),'w')
            f.write('{}')
            f.flush()
            f.close()
            return {}
        elif local == None:
            logger.info('no local version of "%s"'%name)
            return {}
        else:
            return local

    def merge_json(self,default,local):
        lib.helpers.merge(default,local)
