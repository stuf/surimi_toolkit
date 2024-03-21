"""Proof-of-concept of renaming rigs and things belonging to them

   The idea is that things relating to a rig, like geometry, meshes, empties, etc
   are named by the convention of `<type>-<rig_name>-<rest>`,
   and we want to keep `rig_name` consistently named in our projects.

   Naming conventions:
   - separate top/bottom/left/right in the same way as rigify does,
     by suffixing names with `.T`, `.B`, `.L`, `.R` respectively.

   For collections:
   - `GRP` - a collection for something specific
   - `COLL` - collection that contains many collections (that work like alternatives)
   - `META` - off-related or w/e idk

   For objects:
   - `GEO` - geometry
   - `MESH` - the mesh itself in geometry
   - `RIG` - rigs
   - `ARM` - armatures, part of rigs
   - `LTS` - lattices
   - `HLP` - helpers such as empties

   Naming examples:
   - `RIG-character` character rig
   - `GEO-character-eyebrow.L` left eyebrow
   - `GRP-character-body` collection containing things relating to the character's
     body (not including gear)
"""
from bpy import data as D, types as T
import re

RIG_NAME = 'ch01'
NEW_NAME = 'player01'


def main():
    types = {'objects', 'meshes', 'armatures', 'collections'}
    found: list[T.ID] = []

    # re_pat = r'([A-Z]{2,4})\-(' + RIG_NAME + ')'
    re_pat = f'([A-Z]{{2,4}})-({RIG_NAME})'

    print(f'{re_pat=}')

    # look up anything we would want to rename
    for t in types:
        items = getattr(D, t)
        found += [o for o in items if re.search(re_pat, o.name)]

    # now that everything is collected, rename
    for it in found:
        print(f'Found {it=} {it.name=}')
        repl_pat = f'\\1-{NEW_NAME}'
        print(f'  - {repl_pat=}')
        new_name = re.sub(re_pat, repl_pat, it.name)
        print(f'  > {new_name=}')

        it.name = new_name


if __name__ == '__main__':
    main()
