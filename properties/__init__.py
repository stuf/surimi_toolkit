import logging
import bpy
import bpy.types as T

from ..util.register import module_register_factory

logger = logging.getLogger(__name__)

#


MODULES = [
    'collection',
]


reg, unreg = module_register_factory(__name__, MODULES)

#


def register():
    logger.info('registering properties')
    for m in MODULES:
        logger.info(' - module: %s', m)

    reg()


def unregister():
    unreg()
