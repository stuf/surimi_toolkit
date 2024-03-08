import bpy
import re
from typing import List, Dict
from os import listdir
from os.path import join, isfile

UNUSED_X = -600
UNUSED_Y = 0
NORMALMAP_NODE_GROUP = 'RG_Normal_Map'
NORMALMAP_STRENGTH = 0.3  # This needs to be fixed at some point

USE_OCIO_NODEGROUP = True
OCIO_NODEGROUP = 'OCIO_Colorspace'
OCIO_NODENAME = 'OCIOReroute'
SPL_VER_OVERRIDES = 3
TEX_OUT = 'OutTex'

input = {
    'folder': r'W:\Blender\work\__RESOURCES\__ENVIRONMENTS\Fld_SdodrStaffRollBG',
    'image_format': 'tiff',
    'normalmap_strength': 1,
}


cleanup = {'images'}

defaults = {
    'mat_name_separator': '',
    'mat_name_prefix': '',
}


def list_files(dir, fmt):
    return [f for f in listdir(dir) if isfile(join(dir, f)) and f.endswith(fmt)]


def collect_maps(dir, flist: List[str], fmt: str) -> Dict[str, Dict[str, str]]:
    pat = r'(\w+)_(\w{2,3})\.' + f'{fmt}$'
    mats: Dict[str, Dict[str, str]] = dict()

    for f in flist:
        print(f'-> {f}')
        ms = re.findall(pat, f)

        if len(ms) == 0:
            continue

        (base, kind) = ms[0]

        if not base in mats:
            mats[base] = dict()

        mdict = mats[base]
        mdict[kind] = f

    mats_res = dict()

    for (key, value) in mats.items():
        item = dict()

        for (mtype, filename) in value.items():
            cfg = None

            item[mtype] = {
                'maptype': mtype,
                'name': filename,
                'filepath': join(dir, filename),
            }

        mats_res[key] = item

    return mats_res


def _load_img(name, filepath):
    if name in bpy.data.images:
        bpy.data.images.remove(bpy.data.images[name])

    bpy.ops.image.open(filepath=filepath)

    return bpy.data.images[name]


#


def _make_img_tex(nodes, name, filepath, colorspace='sRGB', type='ShaderNodeOctImageTex', gamma=2.2):
    """Create a generic Octane image node"""
    img_tex = nodes.new(type)
    img = _load_img(name, filepath)

    img_tex.image = img
    img.colorspace_settings.name = colorspace

    img_tex.inputs['Legacy gamma'].default_value = 2.2

    return img_tex


# Map handlers


def handle_alb(nodes, maptype=None, filepath=None, name=None):
    tex = _make_img_tex(nodes, name, filepath, gamma=2.2)
    tex.label = maptype
    tex.location = (-400, 600)
    tex.hide = True

    img = tex.image

    outputs = [(tex.outputs[TEX_OUT], nodes['BSDF'].inputs['Base color'])]

    if SPL_VER_OVERRIDES == 2:
        t2 = nodes.new('OctaneAlphaImage')
        t2.image = img
        t2.label = f'{maptype}_opa'
        t2.location = (tex.location[0], tex.location[1] + 50)
        t2.hide = True

        if USE_OCIO_NODEGROUP:
            outputs.append((nodes[OCIO_NODENAME].outputs[0], t2.inputs[1]))

        outputs.append((t2.outputs[TEX_OUT], nodes['BSDF'].inputs['Opacity']))

    return outputs


def handle_ao(nodes, maptype=None, filepath=None, name=None):
    tex = _make_img_tex(nodes, name, filepath)
    tex.label = maptype
    tex.location = (UNUSED_X, UNUSED_Y)
    tex.hide = True

    return [(None, None)]


def handle_rgh(nodes, maptype=None, filepath=None, name=None):
    tex = _make_img_tex(nodes, name, filepath)
    tex.label = maptype
    tex.location = (-400, 400)
    tex.hide = True

    ret = [(tex.outputs[TEX_OUT], nodes['BSDF'].inputs['Specular roughness'])]

    if USE_OCIO_NODEGROUP:
        ret.append((nodes[OCIO_NODENAME].outputs[0], tex.inputs[1]))

    return ret


def handle_mtl(nodes, maptype=None, filepath=None, name=None):
    tex = _make_img_tex(nodes, name, filepath)
    tex.label = maptype
    tex.location = (-400, 500)
    tex.hide = True

    ret = [(tex.outputs[TEX_OUT], nodes['BSDF'].inputs['Metalness'])]

    if USE_OCIO_NODEGROUP:
        ret.append((nodes[OCIO_NODENAME].outputs[0], tex.inputs[1]))

    return ret


def handle_nrm(nodes, maptype=None, filepath=None, name=None):
    inverter = nodes.new('OctaneChannelInverter')
    inverter.inputs[3].default_value = True

    tex = _make_img_tex(nodes, name, filepath)
    tex.label = maptype
    tex.hide = True
    tex.location = (-400, 300)
    # tex.inputs['Power'].default_value = input['normalmap_strength']

    ret = [(tex.outputs[TEX_OUT], inverter.inputs[0]),
           (inverter.outputs[0], nodes['BSDF'].inputs['Normal'])]

    if USE_OCIO_NODEGROUP:
        ret.append((nodes[OCIO_NODENAME].outputs[0], tex.inputs[1]))

    return ret


def handle_opa(nodes, maptype=None, filepath=None, name=None):
    tex = _make_img_tex(nodes, name, filepath, type='OctaneAlphaImage')
    tex.label = maptype
    tex.hide = True
    tex.location = (-400, 200)

    ret = [(tex.outputs['Texture out'], nodes['BSDF'].inputs['Opacity'])]

    if USE_OCIO_NODEGROUP:
        ret.append((nodes[OCIO_NODENAME].outputs[0], tex.inputs[1]))

    return ret


def handle_emm(nodes, maptype=None, filepath=None, name=None):
    tex = _make_img_tex(nodes, name, filepath)
    tex.label = maptype
    tex.hide = True
    tex.location = (UNUSED_X, UNUSED_Y + 50)

    ret = [(None, None)]

    if USE_OCIO_NODEGROUP:
        ret.append((nodes[OCIO_NODENAME].outputs[0], tex.inputs[1]))

    return ret


def handle_emi(nodes, maptype=None, filepath=None, name=None):
    tex = _make_img_tex(nodes, name, filepath)
    tex.label = maptype
    tex.hide = True
    tex.location = (UNUSED_X, UNUSED_Y + 100)

    ret = [(None, None)]

    if USE_OCIO_NODEGROUP:
        ret.append((nodes[OCIO_NODENAME].outputs[0], tex.inputs[1]))

    return ret


def handle_tcl(nodes, maptype=None, filepath=None, name=None):
    tex = _make_img_tex(nodes, name, filepath)
    tex.label = maptype
    tex.hide = True
    tex.location = (UNUSED_X, UNUSED_Y + 200)

    ret = [(None, None)]

    if USE_OCIO_NODEGROUP:
        ret.append((nodes[OCIO_NODENAME].outputs[0], tex.inputs[1]))

    return ret


def handle_spm(nodes, maptype=None, filepath=None, name=None):
    tex = _make_img_tex(nodes, name, filepath)
    tex.label = maptype
    tex.hide = True
    tex.location = (UNUSED_X, UNUSED_Y + 300)

    ret = [(tex.outputs[TEX_OUT], nodes['BSDF'].inputs['Specular weight'])]

    if USE_OCIO_NODEGROUP:
        ret.append((nodes[OCIO_NODENAME].outputs[0], tex.inputs[1]))

    return ret


#


handlers = {
    'Alb': handle_alb,
    'Ao': handle_ao,
    'Rgh': handle_rgh,
    'Mtl': handle_mtl,
    'Nrm': handle_nrm,
    'Opa': handle_opa,
    'Emm': handle_emm,
    'Emi': handle_emi,
    'Tcl': handle_tcl,
    'Spm': handle_spm,
}

#

bsdf_settings = {
    'Smooth shadow terminator': True,
}


def add_material(topname, maps):
    mprefix = '{}{}'.format(
        defaults['mat_name_prefix'], defaults['mat_name_separator'])

    mat_name = f'{mprefix}{topname}'  # -> "Prefix_MatName"

    if mat_name in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials[mat_name])

    mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for node in nodes:
        nodes.remove(node)

    #

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (540, 600)

    if USE_OCIO_NODEGROUP:
        reroute = nodes.new('NodeReroute')
        reroute.location = (-500, 0)
        reroute.name = 'OCIOReroute'

        colorspace = nodes.new('ShaderNodeGroup')
        colorspace.node_tree = bpy.data.node_groups[OCIO_NODEGROUP]
        colorspace.location = (-600, 0)
        colorspace.name = 'OCIO_CS'

        links.new(colorspace.outputs[0], reroute.inputs[0])

    bsdf = nodes.new('OctaneStandardSurfaceMaterial')
    bsdf.name = 'BSDF'
    bsdf.location = (200, 600)
    bsdf.inputs['Smooth shadow terminator'].default_value = True
    bsdf.inputs['Specular weight'].default_value = 0.5

    links.new(bsdf.outputs[0], output.inputs['Surface'])

    for (mtype, mcfg) in maps.items():
        mfile = mcfg['filepath']
        mname = mcfg['name']

        if mtype in handlers:
            handler_func = handlers[mtype]

            res = handler_func(nodes,
                               maptype=mtype,
                               filepath=mfile,
                               name=mname)

            link_items = list()

            if type(res) is tuple:
                link_items.append(res)
            else:
                link_items = res

            for it in link_items:
                (a, b) = it

                if a is not None and b is not None:
                    links.new(a, b)


def add_materials(maps):
    for (k, v) in maps.items():
        add_material(k, v)


#


if __name__ == '__main__':
    fmt = input['image_format']
    files = list_files(input['folder'], fmt)
    maps = collect_maps(input['folder'], files, fmt)

    if 'images' in cleanup:
        image_keys = bpy.data.images.keys()

        for (mname, _) in maps.items():
            for k in image_keys:
                if mname in k:
                    bpy.data.images.remove(bpy.data.images[k])

    add_materials(maps)
