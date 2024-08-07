"""Eliminate duplicate materials that occur when importing multiple models,
   and create a basic shader nodetree setup for them.

   N.B. Currently untested
"""
import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D
from glob import glob

import re
import os.path
from pprint import pprint, pformat
from dataclasses import dataclass
from pathlib import Path

DRY_RUN = False

inpath = r'W:\Blender\work\__RESOURCES\__ENVIRONMENTS'
match_files = f'**/*.png'

#


def find_images(path, glob_pat=None):
    paths = [Path(path, f)
             for f in glob(glob_pat or match_files,
                           root_dir=path)
             # I'm sorry but these have to go
             if not 'BakeDummy00' in f]

    return paths


def find_mat_images(path, mat_name):
    paths = find_images(path, glob_pat=f'**/{mat_name}*.png')

    return paths


def group_images(imgs: list[Path]):
    lookup = {}
    found_types = set()
    found_stems = set()

    for img in imgs:
        # haha regexes
        match = re.match(r'(\w+)_(\w{2,3})\.(\w+)$', img.name)

        if not match:
            print(f'Match: {match=}')
            print(f'Did not get a match for file {img.name}')
            continue

        stem, tex_type, ext = match.groups()

        found_stems.add(stem)
        found_types.add(tex_type)

        if not stem in lookup:
            lookup[stem] = {}

        lookup[stem][tex_type] = img

    return lookup, found_types


def open_image(path: Path):
    # Because the Open Image operator doesn't return the name of the newly opened image,
    # we will be wasteful and just take note of images present before and after the operation,
    # by taking the difference of the two sets.

    images_before = set([img for img in bpy.data.images.keys()])
    print(f'{images_before=}')
    bpy.ops.image.open(filepath=str(path))
    images_after = set([img for img in bpy.data.images.keys()])
    print(f'{images_after=}')
    image_diff = images_before ^ images_after
    print(f'{image_diff=}')

    if not image_diff:
        print(f'Something silly is happening; no images opened')
        raise Exception

    image_name = image_diff.pop()
    image = bpy.data.images[image_name]

    return image


def reassign_duplicates(objects: T.Object):
    """Eliminate duplicate materials, where materials named `Material`,
       `Material_ab` and `Material.###` are considered the same.
    """
    print(f'Reassigning duplicates for {len(objects)} object(s).')

    lookup = {}
    cached = set()

    for obj in objects:
        for slot in obj.material_slots:
            if not slot.material:
                print(f'{slot.name} did not have a material assigned to it')
                continue

            match = re.match(r'(\w+)(_\w{2})?', slot.material.name)
            print(f'match: {match}')

            if not match:
                continue

            # TODO: This feels a bit hacky
            root_name = match.group(1)

            if not root_name in D.materials:
                print(f'{root_name} not found in materials, skipping')
                continue

            if root_name == slot.material.name:
                continue

            print(
                f'Reassigning duplicate material {slot.material.name} to {root_name}')

            if not slot.material.name in lookup:
                lookup[slot.material.name] = root_name

            old_mat_name = slot.material.name

            # Actually reassign the material
            if not DRY_RUN:
                slot.material = D.materials[root_name]

            cached.add((old_mat_name, root_name))

    return cached

#

#


def main():
    print('-----')
    # res = find_images(inpath)
    # res2, textypes = group_images(res)

    # pprint(res2)

    res = find_images(inpath)
    res2, textypes = group_images(res)
    # pprint(res2)
    # print(f'Found {len(textypes)} texture map types; {sorted(textypes)}')

    # take one group for starters
    grp = list(res2.items())
    for k, v in grp:
        print()
        print(f'Material: `{k}`')
        for tex_type, tex_path in v.items():
            print(f'   - {tex_type=}\t{tex_path=}')

    reassign_duplicates(D.objects)


if __name__ == '__main__':
    main()
