import bpy
import bpy.types as T
from bpy import data as D

bl_info = {
    "name": "Surimi Toolkit",
    "author": "piparkaq",
    "version": (0, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Item",
    "description": "Adds a number of useful functions for Splatoon stuff (or in general)",
    "warning": "Experimental",
    "category": "3D View",
}

# LOOKUPS

WEIGHT_LOOKUP = {
    'Leg_1_L': 'DEF-thigh.L',
    'Leg_1_R': 'DEF-thigh.R',
    'Leg_Assist_L': 'DEF-thigh.L.001',
    'Leg_Assist_R': 'DEF-thigh.R.001',
    'Leg_2_L': 'DEF-shin.L',
    'Leg_2_R': 'DEF-shin.R',
    'Ankle_L': 'DEF-foot.L',
    'Ankle_R': 'DEF-foot.R',
    'Ankle_Assist_L': 'DEF-shin.L.001',
    'Ankle_Assist_R': 'DEF-shin.R.001',
    'Toe_L': 'DEF-toe.L',
    'Toe_R': 'DEF-toe.R',
    'Waist': 'DEF-spine',
    'Spine_1': 'DEF-spine.001',
    'Spine_2': 'DEF-spine.002',
    'Spine_3': 'DEF-spine.003',
    'Neck': 'DEF-spine.004',
    'Head': 'DEF-spine.006',
    'Clavicle_L': 'DEF-shoulder.L',
    'Clavicle_R': 'DEF-shoulder.R',
    'Arm_Assist_L': 'DEF-upper_arm.L',
    'Arm_Assist_R': 'DEF-upper_arm.R',
    'Arm_1_L': 'DEF-upper_arm.L.001',
    'Arm_1_R': 'DEF-upper_arm.R.001',
    'Arm_2_L': 'DEF-forearm.L',
    'Arm_2_R': 'DEF-forearm.R',
    'Wrist_Assist_L': 'DEF-forearm.L.001',
    'Wrist_Assist_R': 'DEF-forearm.R.001',
    'Wrist_L': 'DEF-hand.L',
    'Wrist_R': 'DEF-hand.R',
    'Finger_A_1_L': 'DEF-thumb.01.L',
    'Finger_A_2_L': 'DEF-thumb.02.L',
    'Finger_A_3_L': 'DEF-thumb.03.L',
    'Finger_A_1_R': 'DEF-thumb.01.R',
    'Finger_A_2_R': 'DEF-thumb.02.R',
    'Finger_A_3_R': 'DEF-thumb.03.R',
    'Finger_B_1_L': 'DEF-f_index.01.L',
    'Finger_B_2_L': 'DEF-f_index.02.L',
    'Finger_B_3_L': 'DEF-f_index.03.L',
    'Finger_B_1_R': 'DEF-f_index.01.R',
    'Finger_B_2_R': 'DEF-f_index.02.R',
    'Finger_B_3_R': 'DEF-f_index.03.R',
    'Finger_C_1_L': 'DEF-f_middle.01.L',
    'Finger_C_2_L': 'DEF-f_middle.02.L',
    'Finger_C_3_L': 'DEF-f_middle.03.L',
    'Finger_C_1_R': 'DEF-f_middle.01.R',
    'Finger_C_2_R': 'DEF-f_middle.02.R',
    'Finger_C_3_R': 'DEF-f_middle.03.R',
    'Finger_D_1_L': 'DEF-f_ring.01.L',
    'Finger_D_2_L': 'DEF-f_ring.02.L',
    'Finger_D_3_L': 'DEF-f_ring.03.L',
    'Finger_D_1_R': 'DEF-f_ring.01.R',
    'Finger_D_2_R': 'DEF-f_ring.02.R',
    'Finger_D_3_R': 'DEF-f_ring.03.R',
    'Finger_E_1_L': 'DEF-f_pinky.01.L',
    'Finger_E_2_L': 'DEF-f_pinky.02.L',
    'Finger_E_3_L': 'DEF-f_pinky.03.L',
    'Finger_E_1_R': 'DEF-f_pinky.01.R',
    'Finger_E_2_R': 'DEF-f_pinky.02.R',
    'Finger_E_3_R': 'DEF-f_pinky.03.R',
}

# HELPERS


def get_armature(obj: T.Object) -> T.Armature:
    return D.armatures[obj.name]


def is_in_pose_position(armature: T.Armature):
    return armature.pose_position == 'POSE'


# OPERATORS


class OBJECT_OT_surimi_toggle_pose_position(T.Operator):
    bl_idname = 'surimi.toggle_pose_position'
    bl_label = 'Toggle Pose Position'
    bl_description = 'Toggles pose position for the selected armature'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, ctx: T.Context):
        obj = ctx.active_object
        mode = ctx.mode
        armature: T.Armature = obj.data

        armature.pose_position = 'REST' if armature.pose_position == 'POSE' else 'POSE'

        return {'FINISHED'}


class OBJECT_OT_surimi_rename_weights(T.Operator):
    bl_idname = 'surimi.rename_weights'
    bl_label = 'Rename Weights'
    bl_description = 'Rename weights to matching Rigify ones if they exist'
    bl_options = {'REGISTER', 'UNDO'}

    def rename_weights(self, obj: T.Object) -> (bool, int):
        if obj.type != 'MESH':
            return False, 0

        groups: list[str] = obj.vertex_groups

        try:
            renamed = 0

            for g in groups:
                if g.name in WEIGHT_LOOKUP:
                    g.name = WEIGHT_LOOKUP[g.name]
                    renamed += 1

            print(f'Renamed groups; {obj.name=} {renamed=}')
            return True, renamed

        except Exception:
            return False, 0

    def execute(self, ctx: T.Context):
        print(f'RENAME WEIGHTS on {len(ctx.selected_objects)}')
        done_objs = 0
        done_groups = 0

        meshes: list[T.Object] = [
            obj for obj in ctx.selected_objects if obj.type == 'MESH']

        for mesh in meshes:
            res, gs = self.rename_weights(mesh)
            if res:
                done_objs += 1
                done_groups += gs

        if not done_groups:
            self.report(
                {'INFO'},
                'Did not rename any weights for the selected object(s).'
            )

            return {'CANCELLED'}

        self.report(
            {'INFO'},
            f'Renamed: {done_objs=} {done_groups=}'
        )

        return {'FINISHED'}

# UI


class SURIMI_PT_panel_base(T.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'


class SURIMI_PT_panel_main(SURIMI_PT_panel_base):
    bl_idname = 'SURIMI_PT_panel_main'
    bl_label = 'Surimi Toolkit'

    def draw(self, ctx):
        pass


class SURIMI_PT_panel_render(SURIMI_PT_panel_base):
    bl_label = 'Render'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    def draw(self, ctx: T.Context):
        layout = self.layout
        scene = ctx.scene

        layout.use_property_split = True
        layout.use_property_decorate = True

        row = layout.column()
        row.prop(scene.cycles, 'preview_samples', text='Preview')
        row.prop(scene.cycles, 'samples', text='Render')

        layout.separator()

        row = layout.column()
        row.prop(scene.render, 'preview_pixel_size')


class SURIMI_PT_panel_viewport(SURIMI_PT_panel_base):
    bl_label = 'Viewport'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

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
    bl_idname = 'SURIMI_PT_panel_object'
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

# ADDON LIFECYCLE


CLASSES_OPERATORS = [
    OBJECT_OT_surimi_toggle_pose_position,
    OBJECT_OT_surimi_rename_weights,
]

CLASSES_UI = [
    SURIMI_PT_panel_main,
    SURIMI_PT_panel_viewport,
    SURIMI_PT_panel_render,
    SURIMI_PT_panel_armature,
    SURIMI_PT_panel_object,
]

CLASSES = CLASSES_OPERATORS + CLASSES_UI


def register():
    for CLS in CLASSES:
        bpy.utils.register_class(CLS)


def unregister():
    for CLS in reversed(CLASSES):
        bpy.utils.unregister_class(CLS)


if __name__ == '__main__':
    register()
