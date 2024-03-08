import bpy
import bpy.types as T
from bpy import props as P

import logging

logger = logging.getLogger(__name__)


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


class MatImporterProps(T.PropertyGroup):
    search_path: P.StringProperty(
        name='Search path',
        default='W:\\Blender\\work\\__RESOURCES'
    )

    recursive: P.BoolProperty(
        name='Recursive',
        default=True,
    )

    use_material_name: P.BoolProperty(
        name='Use material name for prefix',
        default=True,
    )


#

CLASSES = [
    CharacterProps,
    MatImporterProps,
]

PROPS = [
    ('surimi_props', T.Object, P.PointerProperty(type=CharacterProps)),
    ('surimi_mat_importer', T.Material, P.PointerProperty(type=MatImporterProps)),
]


def register():
    ot_names = [ot.__name__ for ot in CLASSES]
    logger.info('register operators: %s', ot_names)

    for cls in CLASSES:
        bpy.utils.register_class(cls)

    for k, Type, prop in PROPS:
        # Type[k] = prop
        setattr(Type, k, prop)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

    for k, Type, prop in reversed(PROPS):
        delattr(Type, k)


if __name__ == '__main__':
    register()
