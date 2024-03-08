from enum import Enum


class Operators(str, Enum):
    TOGGLE_POSE_POSITION = 'surimi.toggle_pose_position'
    RENAME_WEIGHTS = 'surimi.rename_weights'
    CREATE_CHARACTER_PROPS = 'surimi.create_character_props'

    IMPORT_MATERIAL = 'surimi.import_material'
    CHOOSE_IMPORT_MATERIAL_DIR = 'surimi.choose_import_material_dir'
    RENAME_MATERIAL_TEXTURES = 'surimi.rename_material_textures'


class Panels(str, Enum):
    TOOL_BASE = 'VIEW3D_PT_surimi_base'
    TOOLS = 'SURIMI_PT_panel_main'
    TOOLS_VIEWPORT = 'SURIMI_PT_panel_viewport'
    TOOLS_RENDER = 'SURIMI_PT_panel_render'
    TOOLS_RENDER_OCTANE = 'SURIMI_PT_panel_render_octane'
    TOOLS_ARMATURE = 'SURIMI_PT_panel_armature'
    TOOLS_OBJECT = 'SURIMI_PT_panel_object'
    TOOLS_EXPERIMENTAL = 'SURIMI_PT_panel_experimental'

    NA_HELPERS = 'NA_PT_srm_helpers'
    NA_MAT_IMPORTER = 'NA_PT_srm_node_mat_importer'
    NA_RENAME_IMAGES = 'NA_PT_srm_rename_images'
