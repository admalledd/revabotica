'''loader injection classes, add these as mixins/base classes to get the needed functions'''


#sys imports
import json
import sys
import logging
logger=logging.getLogger('loaders')

#required packages
import fs.opener
import fs.osfs
import fs.mountfs
import fs.multifs
import fs.memoryfs

#local imports
import lib.common

def open_fspaths(fspath):
    '''each map gets its own fs object, we also have a fs.multifs for assest so that a map can over-ride art stuff'''
    def open_dir(subfs,create=False):
        target_path = fs.path.join(subfs,fspath)
        if lib.common.rootfs.isdir(target_path):
            return lib.common.rootfs.opendir(target_path)
        elif create:
            logger.info('creating directory "%s".')
            return lib.common.rootfs.makeopendir(target_path,True)
        else:
            logger.warn('could not open "%s", loading tmpfs instead. if all are tmpfs, bad things happen'%target_path)
            return fs.memoryfs.MemoryFS()

    fsobj = fs.mountfs.MountFS()
    fsobj.mountdir('default',open_dir('default'))
    fsobj.mountdir('custom',open_dir('custom'))
    fsobj.mountdir('save',open_dir(fs.path.join('saves',lib.common.saveid),True))
    multifs = fs.multifs.MultiFS()
    multifs.addfs('default',fs.opener.opener.opendir(fspath))
    #fsobj.tree()
    return fsobj


def load_grid(pyfsobj,gid):
    'convenience helper for loading grid-formated json files'
    return grid_loader(pyfsobj,gid).grid

def load_json(pyfsobj,path):
    'convenience helper for loading normal json files'
    return json_loader(pyfsobj).load_json(path)

class json_loader(object):
    def __init__(self,pyfsobj):
        """load all json files from relevant locations, merge into one, and park it at self.json
        if a file is not found / errors on loading, we skip it and move on. if all fail, we return still
        return {}

        """
        self.pyfsobj = pyfsobj
        self.allow_fail=True

    def load_json(self,name):
        '''loads cfg in the order of: default, u#'s then "local"'''
        default = self.load_json_ro(fs.path.join('default',name))
        custom  = self.load_json_ro(fs.path.join('custom',name))
        saved   = self.load_json_ro(fs.path.join('save',name))

        merged = self.merge_json(default,custom,saved)
        return merged

    def load_json_single(self,fspath):
        '''load one json file, checking if it exists, if it fails for some reason, return {}'''
        try:
            return json.load(self.pyfsobj.open(fspath))
        except fs.errors.ResourceNotFoundError as e:
            if self.allow_fail:
                return {}
            else:
                raise

    def load_json_ro(self,name):
        '''loads json file of $name, if it does not exist, check self.allow_fail'''
        default = self.load_json_single(name)
        if self.allow_fail == True and default == None:
            logger.info('no json file %s, ignoring'%name)
            default = {}
        elif default == None:
            logger.error('no json file %s, returning None...'%name)
            logger.error('not known if this is reachable code...')
            raise
        return default

    def load_json_rw(self,name):
        '''loads json file of $name, if it does not exist, create it.'''
        local = self.load_json_single(fs.path.join('local',name))
        if local == None:
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

    def merge_json(self,*args):
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
        
        default = self.load_json_ro(fs.path.join('default',grid_path))

        if type(default) == list:
            logger.info('loading default "%s" as "full"'%grid_path)
            self.load_grid_full(default)
        elif type(default) == dict and default != {}:
            logger.info('loading default "" as "sparse"'%grid_path)
            self.load_grid_sparse(default)
        else:   
            logger.info('no/bad grid data in default folder')

        custom = self.load_json_ro(fs.path.join('custom',grid_path))
        
        if type(custom) == list:
            logger.info('loading custom "%s" as "full"'%grid_path)
            self.load_grid_full(custom)
        elif type(custom) == dict and custom != {}:
            logger.info('loading custom "%s" as "sparse"'%grid_path)
            self.load_grid_sparse(custom)
        else:
            logger.info('no/bad grid data in custom folder')
        saved = self.load_json_ro(fs.path.join('save',grid_path))

        if type(saved) == list:
            logger.info('loading saved "%s" as "full"'%grid_path)
            self.load_grid_full(saved)
        elif type(saved) == dict and saved != {}:
            logger.info('loading saved "%s" as "sparse"'%grid_path)
            self.load_grid_sparse(saved)
        else:   
            logger.info('no/bad grid data in save folder')

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