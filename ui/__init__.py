import logging
import bpy
import bpy.types as T

from ..util.register import module_register_factory

logger = logging.getLogger(__name__)

ui_modules = [
    'panels',
    'node_editor',
    'collection_properties',
]

reg, unreg = module_register_factory(__name__, ui_modules)


def register():
    logger.info('register UI')
    for m in ui_modules:
        logger.info(' - module: %s', m)

    reg()


def unregister():
    unreg()
