import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

import logging
import re

from ..declarations import Operators as Ot

logger = logging.getLogger(__name__)

#


class SURIMI_OT_character_setup_rename(T.Operator):
    bl_idname = Ot.CHARACTER_SETUP_RENAME
    bl_label = 'Rename Character Setup'
    bl_options = {'REGISTER', 'UNDO'}

    cur_basename: P.StringProperty()
    new_basename: P.StringProperty()

    types = {'objects', 'meshes', 'armatures', 'collections'}

    def execute(self, ctx: T.Context):
        if not self.basename:
            self.report({'ERROR'},
                        'This operator requires a new basename specified. Did you invoke this operator through the UI?')

            return {'CANCELLED'}

        logger.info('Renaming items named `%s` to `%s`',
                    self.cur_basename, self.new_basename)

        cur_name_re = f'([A-Z]{{2,4}})-({self.cur_basename})'
        new_name_re = f'\\1-{self.new_basename}'

        found: list[T.ID] = []

        for t in self.types:
            found += [o for o in getattr(D, t)
                      if re.search(cur_name_re, o.name)]

        logger.info(' - Found %s item(s) to rename', len(found))

        for it in found:
            new_name = re.sub(cur_name_re, new_name_re, it.name)
            it.name = new_name

        return {'FINISHED'}

#


CLASSES = [
    SURIMI_OT_character_setup_rename,
]


def register():
    logger.info('registering operators')

    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
