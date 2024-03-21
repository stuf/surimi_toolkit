import bpy
import bpy.types as T
import bpy.props as P

import logging

from ..util.register import get_name
from ..declarations import Panels as Pt

#

logger = logging.getLogger(__name__)


class SurimiBaseModifierPreferences(T.PropertyGroup):
    """Provides settings used for operators that add modifiers onto objects."""
    expand_bevel: P.BoolProperty(
        name='Expand Bevel modifier in list',
        description='',
        default=False,
    )

    expand_subsurf: P.BoolProperty(
        name='Expand Subdivision modifier in list',
        description='',
        default=False,
    )

    bevel_segments: P.IntProperty(
        name='Bevel segments',
        description='',
        default=2,
    )

    bevel_width: P.FloatProperty(
        name='Bevel width',
        description='',
        default=0.01,
    )


#


class SurimiPreferences:
    """SRM toolkit addon preferences"""
    use_experimental: P.BoolProperty(
        name='Use experimental features',
        default=False,
    )

    base_modifiers: P.PointerProperty(
        name='base modifiers',
        type=SurimiBaseModifierPreferences,
    )

    tab_category: P.StringProperty(
        name='Tab category',
        default='Item',
    )


#


class SurimiAddonPreferences(SurimiPreferences, T.AddonPreferences):
    bl_idname = get_name()

    def draw_base_modifiers(self, ctx: T.Context):
        layout: T.UILayout = self.layout

        col = layout.column()

        grp = col.box().column()
        grp.use_property_split = True
        grp.label(text='General')
        grp.prop(self, 'tab_category')

        grp = col.box().column()
        grp.use_property_split = True
        grp.label(text='Bevel modifier')
        grp.prop(self.base_modifiers, 'expand_bevel')
        grp.prop(self.base_modifiers, 'bevel_segments')
        grp.prop(self.base_modifiers, 'bevel_width')

        grp = col.box().column()
        grp.use_property_split = True
        grp.label(text='Subdivision')
        grp.prop(self.base_modifiers, 'expand_subsurf')

    def draw(self, ctx: T.Context):
        layout: T.UILayout = self.layout

        col = layout.column()

        self.draw_base_modifiers(ctx)


CLASSES = [
    SurimiBaseModifierPreferences,
    SurimiAddonPreferences,
]


def register():
    logger.info('register preferences')

    for cls in CLASSES:
        logger.info(' - class: %s', cls.__name__)
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
