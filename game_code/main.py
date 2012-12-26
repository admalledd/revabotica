import os
import logging

import fs.osfs

import map
import lib.common

##bad global ish stuff here (should not need global state, this is for global logging, fsobj ect)

log_name=os.path.join(lib.common.localdir,'revabotica.log')
# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_name,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger('main')
logger.info('logger set. logging to file:"%s"'%(log_name))
logger.debug('current path: %s'%os.getcwd())
logger.debug('currect localdir: %s'%lib.common.localdir)

lib.common.rootfs=fs.osfs.OSFS('./')#hard coded local for now...

def main():
	m=map.map('maps/test1.map')

def editor():
    '''entry point for the map editor'''
    print "no map editor yet"
