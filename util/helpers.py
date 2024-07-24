from traceback import print_exc
import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

import re
import logging

from typing import Tuple

logger = logging.getLogger(__name__)

#

NAME_PATTERN = r'([A-Z]{2,4})-([\w-]+)(\.\w)?$'
"""Regex pattern for using with common names, useful for
   splitting a name into its prefix/type, name and possible side (`.L`/`.R`)"""

#


def get_armature(obj: T.Object) -> T.Armature:
    return D.armatures[obj.name]


def is_in_pose_position(armature: T.Armature):
    return armature.pose_position == 'POSE'


def render_engine_is(name, ctx: T.Context):
    try:
        return ctx.scene.render.engine == name
    except (AttributeError):
        return False


def render_engine_is_cycles(ctx: T.Context):
    return render_engine_is('CYCLES', ctx)


def render_engine_is_octane(ctx: T.Context):
    return render_engine_is('octane', ctx)

#


def tokenize_name(name: str) -> Tuple[str, str, str | None] | None:
    m = re.match(NAME_PATTERN, name)

    if not m:
        return None

    return m.groups()

#


def pluralize(num: int, term: str):
    return f'{str}{"s"[:num^1]}'
