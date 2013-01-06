import logging
logger=logging.getLogger('entities.parts')

from . import ebase


class scrap(ebase.ebase):
    def load_data(self,fsobj,data):
        super(scrap,self).load_data(fsobj,data)
        self.ammount = data['amount']