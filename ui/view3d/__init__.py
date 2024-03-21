import logging
import bpy
import bpy.types as T

from ...util.register import module_register_factory

logger = logging.getLogger(__name__)

#


MODULES = [

]


reg, unreg = module_register_factory(__name__, MODULES)

#


def register():
    for cls in MODULES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(MODULES):
        bpy.utils.unregister_class(cls)
