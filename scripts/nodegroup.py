import bpy
import bpy.types as T
from bpy import (data as D,
                 context as C,
                 )

grp_name = 'TestGrp'

if not grp_name in D.node_groups:
    print(f'Group {grp_name} already exists, replace it')
    grp = D.node_groups.new(grp_name, 'ShaderNodeTree')
else:
    grp = D.node_groups.get(grp_name)

print(f'{grp=}')

