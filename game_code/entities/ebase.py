import logging
logger=logging.getLogger('entities.ebase')

#import game_code.loaders
from ..loaders import load_img,load_lang

class ebase(object):
    def __init__(self,eid):
        self.eid= eid

    def load_data(self,fsobj,data):
        self.img = load_img(fsobj,data['img'])
        self.lang = load_lang(fsobj,data['lang_file'])
        self.x = data['x']
        self.y = data['y']
        self.data = data
