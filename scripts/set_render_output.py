import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D


def execute():
    rd = C.scene.render
    img = rd.image_settings
    img.file_format = 'TIFF'
    img.color_depth = '16'


if __name__ == '__main__':
    execute()
