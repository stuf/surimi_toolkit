import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

from ...declarations import Operators as Ot

#


#


CLASSES = []


def register():
    for CLS in CLASSES:
        bpy.utils.register_class(CLS)


def unregister():
    for CLS in reversed(CLASSES):
        bpy.utils.unregister_class(CLS)
