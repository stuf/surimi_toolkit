import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

from pprint import pprint
import re

rename_from = 'M_Face'
rename_to = 'octo00-face'


def main():
    imgs = [img for img in D.images if img.name.startswith(rename_from)]

    pprint(imgs)

    for img in imgs:
        _, tex_type = re.match(r'(\w+)_(\w{2,4})', img.name).groups()

        tex_name = f'IMG-{rename_to}-{tex_type}'

        img.name = tex_name


#

if __name__ == '__main__':
    main()
