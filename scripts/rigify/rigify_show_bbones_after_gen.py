import bpy
import bpy.types as T
import bpy.data as D

o = bpy.context.active_object
d: T.Armature = o.data
d.collections['DEF'].is_visible = True
d.display_type = 'BBONE'
