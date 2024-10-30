import logging
import bpy
import bpy.types as T

from ..util.register import module_register_factory

logger = logging.getLogger(__name__)

MODULES = [
    'view3d',
    'node_editor',
    'scripts',
]

reg, unreg = module_register_factory(__name__, MODULES)


def register():
    logger.info('register operators; %s', ', '.join(MODULES))

    reg()


def unregister():
    logger.info('unregister operators; %s', ', '.join(MODULES))

    unreg()
