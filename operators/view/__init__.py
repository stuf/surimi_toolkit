import logging
import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

from ...util.register import module_register_factory
from ...declarations import Operators as Ot

logger = logging.getLogger(__name__)


MODULES = [
    'mesh',
]

reg, unreg = module_register_factory(__name__, MODULES)


def register():
    logger.info('register operators; %s', ', '.join(MODULES))

    reg()


def unregister():
    unreg()
