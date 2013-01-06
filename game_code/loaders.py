'''loader injection classes, add these as mixins/base classes to get the needed functions'''


#sys imports
import json
import sys
import logging
logger=logging.getLogger('loaders')

#required packages
import fs.mountfs
import fs.multifs

#local imports
import lib.common

def open_fspaths(saveid):
    '''each map gets its own fs object, we also have a fs.multifs for assets so that a map can over-ride art stuff'''
    print saveid
    def open_dir(subfs,create=False):
        target_path = fs.path.join(subfs,saveid)
        if lib.common.rootfs.isdir(target_path):
            return lib.common.rootfs.opendir(target_path)
        elif create:
            logger.info('creating directory "%s".')
            return lib.common.rootfs.makeopendir(target_path,True)

    fsobj = fs.mountfs.MountFS()
    fsobj.mountdir('save',open_dir('saves'))

    multifs = fs.multifs.MultiFS()
    multifs.addfs('default',lib.common.rootfs.opendir(fs.path.join('default','assets')))
    multifs.addfs('save',lib.common.rootfs.opendir(fs.path.join('saves',saveid,'assets')))
    #basic files done for the multifs, now to set up the lang file tree. (kinda like a symlink)
    #assets/lang/current/... ---> assets/lang/$lib.common.current_language/...
    
    fsobj.mountdir('assets',multifs)
    fsobj.mountdir('assets/lang/current',multifs.opendir(fs.path.join('lang',lib.common.current_language)))
    fsobj.tree()
    return fsobj


def load_grid(mapobj,gid):
    'convenience helper for loading grid-formated json files'
    return grid_loader(mapobj,gid).grid

def load_json(pyfsobj,path):
    'convenience helper for loading normal json files'
    return json_loader(pyfsobj).load_json(path)

def load_ents(mapobj,layer_id):
    return entity_loader(mapobj,layer_id).entities

class json_loader(object):
    def __init__(self,pyfsobj):
        """load json file from relevant location, parses it, and park it at self.json
        if a file is not found / errors on loading, we skip it and move on. If we fail, we return still
        return {}

        note that we subclass this to add file-type specific parsing / handling.
        """
        self.pyfsobj = pyfsobj
        self.allow_fail=True

    def load_json(self,name):
        '''loads json file. convenience function for the default / common case'''
        return self.load_json_ro(fs.path.join('save',name))

    def load_json_ro(self,name):
        '''loads json file of $name, if it does not exist, check self.allow_fail'''
        try:
            js = json.load(self.pyfsobj.open(name))
        except fs.errors.ResourceNotFoundError as e:
            if self.allow_fail:
                #logger.info('no json file "%s", ignoring'%fspath)
                js = None
            else:
                raise
        
        if self.allow_fail == True and js == None:
            logger.info('no json file %s, ignoring'%name)
            js = {}
        elif js == None:
            logger.error('no json file %s, returning None...'%name)
            raise
        return js
    def merge_json(self,*args):
        '''merge multiple sources of json data (that should now be parsed down to dictionaries) used by subclasses.'''
        merged = {}
        for arg in args:
            merged = lib.helpers.merge(merged,arg)
        return merged

class grid_loader(json_loader):
    def __init__(self,mapobj,gid):
        '''grid format: .grid file is a json file, see docs/grid_format.markdown for more info
        
        there is ALWAYS a grid with GID==0 (the background)

        due to two different ways that the tile info is actually stored (sparse vs full) we pass around:
            initial load, detect, pass off to sub-helpers, merge with self.grid
            we do this for each location that we have to load data from. (default, local, saves)
        '''
        json_loader.__init__(self,mapobj.fsobj)
        self.tile_defaults = mapobj.settings["tile_defaults"]

        self.grid = {}
        self.gid = gid
        self.load_grid()

    def load_grid(self):
        grid_path = fs.path.join('grid','%s.grid'%self.gid)
        
        js = self.load_json_ro(fs.path.join('save',grid_path))

        if type(js) == list:
            logger.info('loading "%s" as "full"'%(grid_path))
            self.load_grid_full(js)
        elif type(js) == dict and js != {}:
            logger.info('loading "%s" as "sparse"'%(grid_path))
            self.load_grid_sparse(js)
        else:   
            logger.info('no/bad grid data in %s'%grid_path)

    def load_grid_full(self,gridlist):
        """load a grid based on a 2d list of dictionaries, see docs/grid_format.markdown for more info"""
        for x,row in enumerate(gridlist):
            for y,cell in enumerate(row):
                self.grid[(x,y)]=self.verify_tile(cell)

    def load_grid_sparse(self,griddict):
        """load a grid from a dictionary of dictionaries"""
        for key,cell in griddict.iteritems():
            x,y=key.split(',')
            x,y = int(x),int(y)
            self.grid[(x,y)]=self.verify_tile(cell)

    def verify_tile(self,tile):
        '''verify that the tile has all the stuff needed, load in defaults if not.'''
        return self.merge_json(self.tile_defaults,tile)

class entity_loader(json_loader):
    def __init__(self,mapobj,layer_id):
        self.entities = {}

        json_loader.__init__(self,mapobj.fsobj)

        e_path = fs.path.join('entities','%s.ejson'%layer_id)

        js = self.load_json_ro(fs.path.join('save',e_path))
        import entities        
        
        for eid,ent_js in js.iteritems():
            ent = entities.entity_classes[ent_js['code_class']](eid)
            ent.load_data(self.pyfsobj,ent_js['data'])
            self.entities[eid]=ent

def load_img(fsobj,path):
    logger.warn('image loading not done yet :D. "%s" would have been loaded.'%path)
    return None

def load_lang(fsobj,path):
    return json_loader(fsobj).load_json_ro(fs.path.join('assets/lang/current',path))