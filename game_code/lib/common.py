import sys,os
import logging
logger = logging.getLogger('lib.common')

import fs.osfs
import fs.path
import fs.opener
import fs.mountfs
import fs.multifs

if sys.platform == 'win32':
    savedir=os.path.expandvars('$APPDATA\\revabotica\\')
else:
    ##TODO:: check if this is the correct save location on MACOSX
    savedir=os.path.expanduser('~/.local/share/revabotica/')

##NOTE::: for testing, over-ride savedir to be local to the code base.
savedir=os.path.join(os.getcwd(),'saves')
rootfs =fs.mountfs.MountFS()
rootfs.mountdir('default',fs.osfs.OSFS('./'))
rootfs.mountdir('saves',fs.osfs.OSFS(savedir))
current_language='en'
#see if we can move all of this stuff to loaders.py, in theory nothing else should need this info.

def p_rents(lo):
    '''
    a function to log where a function got called from
    '''
    import inspect ##because this fuinction should only be called during debug, i dont mind about the 'lag' here
    buf=[]
    for i in reversed(inspect.stack()[1:-1]):
        tmp=[]
        ##first, the path of the script
        if i[1].startswith(curdir):
            filename = i[1][len(curdir)+1:]
        else:
            filename=i[1]
        ##add line number
        lineno = str(i[2])
        ##add class ??? (also, check if it IS a class that we need info from)
        if 'self' in i[0].f_locals:
            cls = str(type(i[0].f_locals['self']))[8:-2]
            cls = str(cls.split('.')[1:])[2:-2]
        else:
            cls = ''
            
        ##add function of class/file
        func = i[3]
        
        buf.append("%s:%s:%s:%s()"%(filename,lineno,cls,func))
        
    path=" >> ".join(buf)
    ##finaly, use logging instance to log thins thing for us, saving it to file, printing to terminal and whatnot
    lo.debug('call stack: %s'%path)