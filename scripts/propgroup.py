import bpy
import bpy.types as T
from bpy import props as P

PROPS = [
    ('surimi_root', T.Object, P.BoolProperty()),
]


def register():
    for k, Type, prop in PROPS:
        setattr(Type, k, prop)


def unregister():
    for k, Type, _ in PROPS:
        delattr(Type, k)


if __name__ == '__main__':
    register()
