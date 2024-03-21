import logging

from bpy import data as D, context as C
import bpy.types as T

logger = logging.getLogger(__name__)


def get_armature(obj: T.Object) -> T.Armature:
    return D.armatures[obj.name]


def is_in_pose_position(armature: T.Armature):
    return armature.pose_position == 'POSE'


def is_octane_render_present():
    return 'octane' in C.preferences.addons


def render_engine_is_cycles():
    try:
        return C.scene.render.engine == 'cycles'
    except (AttributeError):
        return False


def render_engine_is_octane():
    try:
        return C.scene.render.engine == 'octane'
    except (AttributeError):
        return False

#


def pluralize(num: int, term: str):
    return f'{str}{"s"[:num^1]}'
