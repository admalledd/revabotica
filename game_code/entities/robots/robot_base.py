import logging
logger=logging.getLogger('entities.robots.robot_base')

from .. import entity_base


class robot(entity_base.entity_base):
    def load_data(self,fsobj,data):
        super(robot,self).load_data(fsobj,data)
        self.name = data['name']