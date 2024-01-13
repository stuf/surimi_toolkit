import bpy
import bpy.types as T
from bpy import props as P


class CharacterProps(T.PropertyGroup):
    character_color_1: P.FloatVectorProperty(
        name='Primary',
        description='Primary player color',
        subtype='COLOR',
        default=(0.631, 0.515, 0.002),
        min=0.0,
        max=1.0,
    )

    character_color_2: P.FloatVectorProperty(
        name='Secondary',
        description='Secondary player color',
        subtype='COLOR',
        default=(0.042, 0.004, 0.610),
        min=0.0,
        max=1.0,
    )

    eye_pupil_size: P.FloatProperty(
        name='Eye pupil size',
        description='Eye pupil size',
        min=-1.0,
        max=1.0,
    )

    eye_pupil_depth: P.FloatProperty(
        name='Eye pupil depth',
        description='Eye pupil depth',
        min=-1.0,
        max=1.0,
    )

    skin_tone_1: P.FloatVectorProperty(
        name='Skin Tone 1',
        description='Top skin layer color',
        subtype='COLOR',
        default=(0.971, 0.862, 0.604),
        min=0.0,
        max=1.0,
    )

    skin_tone_2: P.FloatVectorProperty(
        name='Skin Tone 2',
        description='Mid skin layer color',
        subtype='COLOR',
        default=(0.386, 0.109, 0.047),
        min=0.0,
        max=1.0,
    )

    skin_tone_3: P.FloatVectorProperty(
        name='Skin Tone 3',
        description='Shine-through (scatter) skin color',
        subtype='COLOR',
        default=(0.451, 0.019, 0.005),
        min=0.0,
        max=1.0,
    )

#


classes = [
    CharacterProps,
]

parent_type = T.Object


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    parent_type.surimi_props = P.PointerProperty(type=CharacterProps)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del parent_type.surimi_props


if __name__ == '__main__':
    register()
