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
    	self.settings=loaders.load_json(self.fsobj,'config.json')

        print loaders.load_grid(self,0)

