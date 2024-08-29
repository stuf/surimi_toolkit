from enum import Enum


class Operators(str, Enum):
    # View3D
    TOGGLE_POSE_POSITION = 'surimi.toggle_pose_position'
    RENAME_WEIGHTS = 'surimi.rename_weights'
    CREATE_CHARACTER_PROPS = 'surimi.create_character_props'
    SET_SUBDIV_DISPLAY = 'surimi.set_subdiv_display'

    # Nodes
    IMPORT_MATERIAL = 'surimi.import_material'
    CHOOSE_IMPORT_MATERIAL_DIR = 'surimi.choose_import_material_dir'
    RENAME_MATERIAL_TEXTURES = 'surimi.rename_material_textures'
    ADD_IMAGETEX = 'surimi.add_imagetex'
    ADD_NODE = 'surimi.add_node'
    NORMALIZE_SELECTED_FILENAMES = 'surimi.normalize_selected_filenames'

    # Experimental
    CHARACTER_SETUP_RENAME = 'surimi.character_setup_rename'
    ADD_USUAL_MODIFIERS = 'surimi.add_usual_modifiers'
    TOGGLE_BONE_COLLECTION = 'surimi.toggle_bone_collection'
    EXPERIMENTAL_NORMALIZE_IMAGE_NODES = 'surimi.experimental_normalize_image_nodes'

    EXPERIMENTAL_SCRIPT_MAKE_REF_ENV = 'surimi.script_make_ref_environment'

    EXPERIMENTAL_IMPORT_MAP_MATERIALS = 'surimi.experimental_import_map_materials'


class Panels(str, Enum):
    TOOL_BASE = 'VIEW3D_PT_surimi_base'
    TOOLS = 'SURIMI_PT_panel_main'
    TOOLS_VIEWPORT = 'SURIMI_PT_panel_viewport'
    TOOLS_RENDER = 'SURIMI_PT_panel_render'
    TOOLS_RENDER_OCTANE = 'SURIMI_PT_panel_render_octane'
    TOOLS_ARMATURE = 'SURIMI_PT_panel_armature'
    TOOLS_OBJECT = 'SURIMI_PT_panel_object'
    TOOLS_EXPERIMENTAL = 'SURIMI_PT_panel_experimental'

    TOOLS_BONE_COLLECTIONS = 'SURIMI_PT_bone_collections'

    NA_HELPERS = 'NA_PT_srm_helpers'
    NA_NORMALIZE_SELECTED_FILENAMES = 'NA_PT_srm_normalize_selected_filenames'
    NA_MAT_IMPORTER = 'NA_PT_srm_node_mat_importer'
    NA_RENAME_IMAGES = 'NA_PT_srm_rename_images'
    NA_QUICK_NODES = 'NA_PT_srm_quick_nodes'
    NA_OTHER = 'NA_PT_srm_node_other'

    PREFS_BASE_MODIFIER_SETTINGS = 'SURIMI_PT_prefs_base_modifier_settings'

#


class NodeColor(Enum):
    MAT_GROUP = (0.2240482121706009, 0.284084677696228, 0.21454641222953796)
    PARAM_GROUP = (0.4942544996738434, 0.3937067687511444, 0.6079999804496765)
    TEX_GROUP = (0.38551008701324463, 0.47391942143440247, 0.6079999804496765)
    UTIL_GROUP = (0.393707, 0.608, 0.48417)
