import bpy
import logging

from ..util.register import module_register_factory

logger = logging.getLogger(__name__)

base_modules = [
    'preferences',
]

reg, unreg = module_register_factory(__name__, base_modules)


def register():
    logger.info('registering base modules')
    for m in base_modules:
        logger.info(' - module: %s', m)

    reg()


def unregister():
    unreg()
