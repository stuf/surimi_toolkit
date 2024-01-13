import bpy
import bpy.types as T
from bpy import props as P


class CustomGroup(T.PropertyGroup):
    character_color_1: P.FloatVectorProperty(
        name='color_1-123',
        description='Primary player color',
        subtype='COLOR',
        default=(0.631, 0.515, 0.002),
        min=0.0,
        max=1.0,
    )

    skin_tone_1: P.FloatVectorProperty(
        name='skin_tone_1',
        description='Top skin layer color',
        subtype='COLOR',
        min=0.0,
        max=1.0,
    )

    skin_tone_2: P.FloatVectorProperty(
        name='skin_tone_2',
        description='Mid skin layer color',
        subtype='COLOR',
        min=0.0,
        max=1.0,
    )

    skin_tone_3: P.FloatVectorProperty(
        name='skin_tone_3',
        description='Shine-through (scatter) skin color',
        subtype='COLOR',
        min=0.0,
        max=1.0,
    )

#


classes = [
    CustomGroup,
]

parent_type = T.Object


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    parent_type.surimi_props = P.PointerProperty(type=CustomGroup)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del parent_type.surimi_props


if __name__ == '__main__':
    register()
