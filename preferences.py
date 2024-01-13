import bpy
import bpy.types as T
import bpy.props as P


class AddonPreferences(T.AddonPreferences):
    bl_idname = __package__

    use_experimental: P.BoolProperty(
        name='Use experimental features',
        default=False,
    )

    def draw(self, ctx: T.Context):
        layout: T.UILayout = self.layout

        col = layout.column()

        grp = col.box().column()
        grp.label(text='Experimental')
        grp.prop(self, 'use_experimental')
        grp.label(text='These features are not properly tested or finalized.')


classes = [
    AddonPreferences,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
