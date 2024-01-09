import logging

from bpy import data as D
import bpy.types as T

logger = logging.getLogger(__name__)


def get_armature(obj: T.Object) -> T.Armature:
    return D.armatures[obj.name]


def is_in_pose_position(armature: T.Armature):
    return armature.pose_position == 'POSE'

#


def pluralize(num: int, term: str):
    return f'{str}{"s"[:num^1]}'
