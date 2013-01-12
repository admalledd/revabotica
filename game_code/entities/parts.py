import logging
logger=logging.getLogger('entities.parts')

from . import entity_base


class scrap(entity_base.entity_base):
    def load_data(self,fsobj,data):
        super(scrap,self).load_data(fsobj,data)
        self.ammount = data['amount']