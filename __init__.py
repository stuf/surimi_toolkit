import logging

from .util.register import module_register_factory
from .util.logging import setup_logger

bl_info = {
    "name": "Surimi Toolkit",
    "author": "piparkaq",
    "version": (0, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Item",
    "description": "Adds a number of useful functions for Splatoon stuff (or in general)",
    "warning": "Experimental",
    "category": "3D View",
}

logger = logging.getLogger(f'{__name__}_MAIN')

# ====
# INIT

base_modules = [
    'operators',
    'ui',
]

reg, unreg = module_register_factory(__name__, base_modules)

# ADDON LIFECYCLE


def register():
    setup_logger(logger)

    logger.info('Registering addon; %s', bl_info)

    reg()

    # for CLS in CLASSES:
    #     bpy.utils.register_class(CLS)


def unregister():
    unreg()
    # for CLS in reversed(CLASSES):
    #     bpy.utils.unregister_class(CLS)


if __name__ == '__main__':
    register()
