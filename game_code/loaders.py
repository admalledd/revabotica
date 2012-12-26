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

#local imports
import lib.common

def open_fspaths(fspath):
    '''each map gets its own fs object, we also have a fs.multifs for assest so that a map can over-ride art stuff'''
    fsobj = fs.mountfs.MountFS()
    fsobj.mountdir('default',lib.common.rootfs.opendir(fspath))
    fsobj.mountdir('local',fs.osfs.OSFS(fs.path.join(lib.common.localdir,fspath), create=True))
    multifs = fs.multifs.MultiFS()
    multifs.addfs('default',fs.opener.opener.opendir(fspath))
    fsobj.tree()
    return fsobj

