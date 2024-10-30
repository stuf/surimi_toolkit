bl_info = {
    "name": "Surimi Toolkit",
    "category": "3D View",
    "author": "piparkaq",
    "version": (0, 7, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Item",
    "description": "Adds a number of useful functions for Splatoon stuff (or in general)",
    "warning": "Experimental",
    "doc_url": "https://github.com/stuf/surimi_toolkit",
    "tracker_url": "https://github.com/stuf/surimi_toolkit/issues"
}

from .util.register import module_register_factory, cleanse_modules
from .util.preferences import get_prefs
from .util.logging import setup_logger
import bpy.types as T
import logging

logger = logging.getLogger(f'{__name__}_MAIN')

# ====
# INIT

base_modules = [
    'base',
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
