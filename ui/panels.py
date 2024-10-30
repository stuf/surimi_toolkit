import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C
import logging

from ..declarations import Panels as Pt, Operators as Ot
from ..util.helpers import is_in_pose_position, render_engine_is_cycles, render_engine_is_octane
from ..util.preferences import is_experimental

from ..operators.view3d import (OBJECT_OT_surimi_rename_weights,
                                OBJECT_OT_surimi_toggle_pose_position,
                                OBJECT_OT_surimi_set_subdiv_display,
                                )

logger = logging.getLogger(__name__)

#


class SURIMI_PT_panel_base(T.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Surimi'
    bl_order = 1


class SURIMI_PT_panel_main(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS
    bl_label = 'Surimi Toolkit'

    def draw(self, ctx):
        pass

#


class SURIMI_PT_panel_render_octane(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS_RENDER_OCTANE
    bl_label = 'Render (Octane)'

    @classmethod
    def poll(cls, ctx: T.Context):
        return render_engine_is_octane(ctx)

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

    @classmethod
    def poll(cls, ctx: T.Context):
        return render_engine_is_cycles(ctx)

    def draw(self, ctx: T.Context):
        layout = self.layout
        scene = ctx.scene

        layout.use_property_split = True
        layout.use_property_decorate = True

        if render_engine_is_cycles(ctx):
            row = layout.column(align=True)
            row.prop(scene.cycles, 'preview_samples', text='Preview')
            row.prop(scene.cycles, 'samples', text='Render')

        layout.separator()

        row = layout.column()
        row.prop(scene.render, 'preview_pixel_size')


class SURIMI_PT_panel_viewport(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS_VIEWPORT
    bl_label = 'Viewport'

    def draw(self, ctx: T.Context):
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

    @classmethod
    def poll(cls, ctx: T.Context):
        return any(x.type == 'MESH' for x in ctx.selected_objects)

    def draw(self, ctx: T.Context):
        layout = self.layout
        obj = ctx.active_object

        row = layout.column()
        row.operator(OBJECT_OT_surimi_rename_weights.bl_idname)

        layout.separator()

        row = layout.column()
        row.label(text="Subdiv. optimal display")

        row = layout.row(align=True)
        subdiv_optimal_enable = row.operator(
            OBJECT_OT_surimi_set_subdiv_display.bl_idname, text="Enable")
        subdiv_optimal_enable.set_value = True

        subdiv_optimal_disable = row.operator(
            OBJECT_OT_surimi_set_subdiv_display.bl_idname, text="Disable")
        subdiv_optimal_disable.set_value = False


class SURIMI_PT_panel_mesh(SURIMI_PT_panel_base):
    bl_idname = Pt.TOOLS_MESH
    bl_label = 'Mesh'

    @classmethod
    def poll(cls, ctx: T.Context):
        mesh_selected = ctx.active_object.type == 'MESH'
        in_edit_mode = ctx.mode == 'EDIT_MESH'
        return mesh_selected and in_edit_mode

    def draw(self, ctx: T.Context):
        layout = self.layout
        obj = ctx.active_object

        row = layout.column()
        row.label(text='ASK:DJ')
        row.label(text=f'Current mode: {ctx.mode}')

#


classes = [
    SURIMI_PT_panel_viewport,
    SURIMI_PT_panel_render,
    SURIMI_PT_panel_render_octane,
    SURIMI_PT_panel_object,
    SURIMI_PT_panel_armature,
    SURIMI_PT_panel_mesh,
]


def register():
    logger.info('registering UI')
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
