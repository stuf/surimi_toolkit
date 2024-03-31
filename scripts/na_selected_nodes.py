import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

import re

# TODO: Allow support to match `alb` and `Alb`
gamma = [
    ({'alb'}, 2.2),
]


def main():
    print('-----')
    # Only consider these kinds of RNA identifiers (in this context "node types")
    node_rna_types = {'ShaderNodeOctImageTex', 'OctaneRGBImage'}
    name_pat = r'(\w+)_(\w{2,4})(\.\w+)?$'

    obj = C.active_object
    mat = obj.active_material
    mat_name = mat.name
    nodes = mat.node_tree.nodes

    # Get selected nodes and filter out non-images
    selected: list[T.Node] = \
        [n
         for n in nodes
         if n.select
         and n.bl_rna.identifier in node_rna_types]

    # Normalize names and gamma for valid image nodes encountered
    for n in selected:
        print(f'{n=}')
        img: T.Image = n.image
        img_name = img.name

        if not img_name.startswith(mat_name):
            print(
                f'Image name `{img_name=}` does not start with `{mat_name=}`, skipping.')
            continue

        tail = img_name.removeprefix(f'{mat_name}_')
        tail = re.match(r'(\w+)', tail)

        if not tail:
            print('Something silly going on')
            print(f' - {img_name=}')
            print(f' - {mat_name=}')
            print(f' - {tail=}')
            continue

        tail = tail.group(1).lower()
        n.image.name = '-'.join([mat_name, tail])
        n.label = tail
        n.name = f'NODE-{n.image.name}'

        # This only works if you have Octane
        # Essentially should change the colorspace if in Cycles/Eevee
        for types, gamma_value in gamma:
            socket = n.inputs['Legacy gamma']
            if tail in types or tail.capitalize() in types:
                socket.default_value = gamma_value
            else:
                socket.default_value = 1.0


if __name__ == '__main__':
    main()
