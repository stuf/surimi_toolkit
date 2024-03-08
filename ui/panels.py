import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C
import logging

from ..declarations import Panels as Pt, Operators as Ot
from ..util.helpers import is_in_pose_position
from ..util.preferences import is_experimental

from ..operators.view3d import (OBJECT_OT_surimi_rename_weights,
                                OBJECT_OT_surimi_toggle_pose_position,
                                )

logger = logging.getLogger(__name__)


class SURIMI_PT_panel_base(T.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Surimi'


class SURIMI_PT_panel_main(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS
    bl_label = 'Surimi Toolkit'

    def draw(self, ctx):
        pass


class SURIMI_PT_panel_render_octane(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS_RENDER_OCTANE
    bl_label = 'Render (Octane)'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    @classmethod
    def poll(cls, ctx: T.Context):
        return ctx.scene.render.engine == 'octane'

    def draw(self, ctx: T.Context):
        layout = self.layout
        scene = ctx.scene

        layout.use_property_decorate = True
        layout.use_property_split = True

        row = layout.column()
        row.prop(scene.oct_view_cam.imager, 'up_sample_mode')


class SURIMI_PT_panel_render(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS_RENDER
    bl_label = 'Render'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    @classmethod
    def poll(cls, ctx: T.Context):
        return ctx.scene.render.engine == 'cycles'

    def draw(self, ctx: T.Context):
        layout = self.layout
        scene = ctx.scene

        layout.use_property_split = True
        layout.use_property_decorate = True

        if scene.render.engine == 'octane':
            pass

        if scene.render.engine == 'cycles':
            row = layout.column()
            row.prop(scene.cycles, 'preview_samples', text='Preview')
            row.prop(scene.cycles, 'samples', text='Render')

        layout.separator()

        row = layout.column()
        row.prop(scene.render, 'preview_pixel_size')


class SURIMI_PT_panel_viewport(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS_VIEWPORT
    bl_label = 'Viewport'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    def draw(self, ctx: T.Context):
        logger.info('Render Settings', ctx.scene.render.engine)

        layout = self.layout
        scene = ctx.scene

        layout.use_property_split = True
        layout.use_property_decorate = True

        row = layout.column()
        row.prop(scene.render, 'use_simplify')

        row = layout.column()
        row.enabled = scene.render.use_simplify
        row.prop(scene.render, 'simplify_subdivision')


class SURIMI_PT_panel_armature(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS_ARMATURE
    bl_label = 'Armature'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    @classmethod
    def poll(cls, ctx: T.Context):
        try:
            return ctx.active_object.type == 'ARMATURE'
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, ctx: T.Context):
        layout = self.layout

        obj = ctx.active_object
        armature: T.Armature = obj.data

        in_pose_position = is_in_pose_position(armature)

        layout = self.layout

        row = layout.column()
        row.operator(OBJECT_OT_surimi_toggle_pose_position.bl_idname,
                     text='Pose mode', depress=in_pose_position)


class SURIMI_PT_panel_object(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS_OBJECT
    bl_label = 'Object'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    @classmethod
    def poll(cls, ctx: T.Context):
        return any(x.type == 'MESH' for x in ctx.selected_objects)

    def draw(self, ctx: T.Context):
        layout = self.layout
        obj = ctx.active_object

        row = layout.column()
        row.operator(OBJECT_OT_surimi_rename_weights.bl_idname)


#

class SURIMI_PT_panel_experimental(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS_EXPERIMENTAL
    bl_label = 'Experimental'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    @classmethod
    def poll(cls, ctx: T.Context):
        return is_experimental()

    def draw(self, ctx: T.Context):
        layout = self.layout
        obj = ctx.active_object
        props = obj.surimi_props

        col = layout.column(align=True)
        col.enabled = False

        row = col.column()
        row.operator(Ot.CREATE_CHARACTER_PROPS)
        row.operator(Ot.CREATE_CHARACTER_PROPS, text="Create Nodegroups")

        col.separator()

        row = col.box().row()
        row.prop(props, 'character_color_1')

        row = col.box().row()
        row.prop(props, 'character_color_2')

        col.separator()

        row = col.box().row()
        row.prop(props, 'skin_tone_1')

        row = col.box().row()
        row.prop(props, 'skin_tone_2')

        row = col.box().row()
        row.prop(props, 'skin_tone_3')

        col.separator()

        row = col.box().row()
        row.prop(props, 'eye_pupil_size')

        row = col.box().row()
        row.prop(props, 'eye_pupil_depth')


#

classes = [
    SURIMI_PT_panel_main,
    SURIMI_PT_panel_viewport,
    SURIMI_PT_panel_render,
    SURIMI_PT_panel_render_octane,
    SURIMI_PT_panel_object,
    SURIMI_PT_panel_armature,
    SURIMI_PT_panel_experimental,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
