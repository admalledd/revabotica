'''loader injection classes, add these as mixins/base classes to get the needed functions'''


#sys imports
import json
import sys,os
import struct

#required packages
import fs.opener
import fs.osfs
import fs.mountfs
import fs.path
import fs.errors

#local imports
import lib.helpers


if sys.platform == 'win32':
    localdir=os.path.expandvars('$APPDATA\\revabotica\\')
else:
    #TODO:: check for correct save locations on linux/macosx
    localdir=os.path.expanduser('~/.revabotica/')


class json_mixin(object):
    ''''''    
    def load_cfg(self,name):
        '''loads cfg in the order of: default, u#'s then "local"'''
        default = json.load(self.fsobj.open(fs.path.join('/default',name)))
        try:
            local = json.load(self.fsobj.open(fs.path.join('/local',name)))
        except fs.errors.ResourceNotFoundError as e:
            #could not open file, no local copy exists. create a blank one and use that
            print 'no local version of %s, creating blank'%name
            f=self.fsobj.open(fs.path.join('/local',name),'w')
            f.write('{}')
            f.flush()
            f.close()
            local = {}
        
        
        return lib.helpers.merge(default,local)

class fs_load_mixin(object):
    def open_fspaths(self,fspath):
        self.fsobj = fs.mountfs.MountFS()
        self.fsobj.mountdir('default',fs.opener.opener.opendir(fspath))
        self.fsobj.mountdir('local',fs.osfs.OSFS(fs.path.join(localdir,fspath), create=True))
        #self.fsobj.tree()

class grid_mixin(object):
    def load_grid(self,gid):
        '''grid format: .grid file is arranged with a struct of whatever is in the config.json for that map.
           no overrides of the grid layout is allowed :C have to keep it the same for all layers to prevent overdraw.

        now, note that tile grids are always in pairs with entity layers, so this mixin actually also has the entity code
        also there is ALWAYS a grid with GID==0 (the background)
        '''

        #first, get config settings for our structs
        class tile(object):pass #we use setattr on this class to add all our stuff
        fmt=[]
        for attr in self.settings["tile_struct"]:
            setattr(tile,attr.keys()[0],None)
            fmt.append(attr.items()[0][1])
        fmt = ''.join(fmt)
