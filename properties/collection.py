import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

import logging

#

logger = logging.getLogger(__name__)


#

class SurimiCollectionProperties(T.PropertyGroup):
    pass

#


CLASSES = [
    SurimiCollectionProperties,
]

PROPS = [
    (
        'surimi_setup_root',
        T.Collection,
        P.BoolProperty(
            default=False, description='Mark this collection as a root containing a character setup'),
    ),
    (
        'surimi_setup',
        T.Collection,
        P.PointerProperty(type=SurimiCollectionProperties),
    ),
]


def register():
    logger.info('registering properties')

    for cls in CLASSES:
        logger.info(' - class: %s', cls.__name__)
        bpy.utils.register_class(cls)

    for k, Type, prop in PROPS:
        logger.info(' - property: %s', k)
        setattr(Type, k, prop)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

    for k, Type, _ in PROPS:
        delattr(Type, k)
