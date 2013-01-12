import logging
logger=logging.getLogger('entities')

from . import parts
import robots

entity_classes = {'parts.scrap':parts.scrap}

entity_classes.update(robots.robot_classes)
