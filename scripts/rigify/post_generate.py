import bpy
from typing import Literal, Tuple
from mathutils import Vector
import bpy.types as T
from bpy.types import Armature, Bone, PoseBone, BoneColor, Object
from dataclasses import dataclass

BoneDisplayType = Literal['OCTAHEDRAL', 'STICK', 'BBONE', 'ENVELOPE', 'WIRE']

ColorT = Tuple[float, float, float]


# Color sets

@dataclass
class BoneColorPalette:
    regular: ColorT
    selected: ColorT
    active: ColorT


Palette = {
    # Theme color 11
    'master_bone': BoneColorPalette(
        (0.360784, 0.611765, 1.0),
        (0.513726, 0.741176, 1.0),
        (0.886275, 0.952941, 1.0),
    ),
    # Theme color 2
    'parent_bone': BoneColorPalette(
        (1.0,      0.478431, 0.101961),
        (1.0,      0.639216, 0.360784),
        (1.0,      0.917647, 0.862745),
    ),
    # Theme color 4
    'control_bone': BoneColorPalette(
        (0.984314, 0.784314, 0.0),
        (1.0,      0.921569, 0.0),
        (0.980392, 0.94902,  0.831373),
    ),
    # Theme color 6
    'glue_bone': BoneColorPalette(
        (0.737255, 0.882353, 0.0),
        (0.866667, 1.0,      0.231373),
        (0.933333, 0.964706, 0.85098),
    ),
    # Theme color 7
    'stretch_bone': BoneColorPalette(
        (0.117647, 0.917647, 0.443137),
        (0.431373, 1.0,      0.603922),
        (0.878431, 0.980392, 0.894118),
    ),

    # Theme color 20
    'display_bone': BoneColorPalette(
        (0.654902, 0.631373, 0.709804),
        (0.760784, 0.717647, 0.854902),
        (0.956863, 0.937255, 0.996078),
    )
}


# Bone config

@dataclass
class BoneConfig:
    bones: list[str]
    width: float = None
    display_type: BoneDisplayType = None
    color_set: BoneColorPalette = None

    def prefix_name(self, bone: str):
        if self.bone_prefix is None:
            return bone

        return f'{self.bone_prefix}-{bone}'

    def set_bone_color(self, bone: T.PoseBone):
        if not self.color_set:
            return

        bone.color.palette = 'CUSTOM'
        color_set: T.ThemeBoneColorSet = bone.color.custom
        color_set.active = self.color_set.active
        color_set.normal = self.color_set.regular
        color_set.select = self.color_set.selected


Primary = BoneConfig(
    bones=[
        'hips',
        'torso',
        'chest',
        'head',

        'hand_ik.L',
        'hand_ik.R',
        'foot_ik.L',
        'foot_ik.R',
    ],
    width=2.0,
    color_set=Palette['control_bone']
)

MouthMCH = BoneConfig(
    bones=[
        'DEF-lip_point.T',
        'DEF-lip_point.B',
        'DEF-lip_point.L',
        'DEF-lip_point.R',
        'DEF-lip_point.T.L',
        'DEF-lip_point.T.R',
        'DEF-lip_point.B.L',
        'DEF-lip_point.B.R',
    ],
    display_type='WIRE',
    color_set=Palette['stretch_bone']
)

#


def get_bone(bone_name, obj: T.Object):
    armature: T.Armature = obj.data
    b = armature.bones[bone_name]
    pb = obj.pose.bones[bone_name]

    return b, pb


def set_bone_color(color: BoneColorPalette, bone: T.PoseBone):
    bone.color.palette = 'CUSTOM'
    color_set: T.ThemeBoneColorSet = bone.color.custom
    color_set.active = color.active
    color_set.normal = color.regular
    color_set.select = color.selected


#

o = bpy.context.active_object
d: Armature = o.data
d.collections['DEF'].is_visible = True
d.display_type = 'STICK'

for bone in Primary.bones:
    b, pb = get_bone(bone, o)
    o.pose.bones[bone].custom_shape_wire_width = Primary.width

    Primary.set_bone_color(pb)

# Fix extra mouth MCH bones
for bone in MouthMCH.bones:
    b, pb = get_bone(bone, o)

    b.display_type = MouthMCH.display_type
    MouthMCH.set_bone_color(pb)
