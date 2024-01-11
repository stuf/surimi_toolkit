from enum import Enum


class Operators(str, Enum):
    TOGGLE_POSE_POSITION = 'surimi.toggle_pose_position'
    RENAME_WEIGHTS = 'surimi.rename_weights'
    CREATE_CHARACTER_PROPS = 'surimi.create_character_props'


class Panels(str, Enum):
    TOOL_BASE = 'VIEW3D_PT_surimi_base'
    TOOLS = 'SURIMI_PT_panel_main'
    TOOLS_VIEWPORT = 'SURIMI_PT_panel_viewport'
    TOOLS_RENDER = 'SURIMI_PT_panel_render'
    TOOLS_ARMATURE = 'SURIMI_PT_panel_armature'
    TOOLS_OBJECT = 'SURIMI_PT_panel_object'
