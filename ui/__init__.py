import logging
import bpy
import bpy.types as T

from ..util.register import module_register_factory

logger = logging.getLogger(__name__)

ui_modules = [
    'panels',
    'node_editor',
]

reg, unreg = module_register_factory(__name__, ui_modules)


def register():
    logger.info('Register UI')
    logger.info(' - modules: %s', ui_modules)
    reg()


def unregister():
    logger.info('Unregister UI')
    unreg()
