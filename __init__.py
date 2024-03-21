bl_info = {
    "name": "Surimi Toolkit",
    "category": "3D View",
    "author": "piparkaq",
    "version": (0, 5, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Item",
    "description": "Adds a number of useful functions for Splatoon stuff (or in general)",
    "warning": "Experimental",
    "doc_url": "https://github.com/stuf/surimi_toolkit",
    "tracker_url": "https://github.com/stuf/surimi_toolkit/issues"
}

import logging
import bpy.types as T

from .util.register import module_register_factory, cleanse_modules
from .util.logging import setup_logger
from .util.preferences import get_prefs

logger = logging.getLogger(f'{__name__}_MAIN')

# ====
# INIT

base_modules = [
    'base',
    'properties',
    'operators',
    'ui',
]

reg, unreg = module_register_factory(__name__, base_modules)


# ADDON LIFECYCLE

def register():
    setup_logger(logger)

    logger.info('register addon')

    reg()


def unregister():
    unreg()

    cleanse_modules(__package__)


#

if __name__ == '__main__':
    register()
