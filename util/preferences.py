import bpy

from .register import get_name


def get_prefs():
    addon_name = get_name()
    addons = bpy.context.preferences.addons.keys()

    print(f'{addon_name=}')
    print(f'{addons=}')
    has_srm = [n for n in addons if n.find('surimi')]
    print(f'{has_srm=}')
    return bpy.context.preferences.addons[get_name()].preferences


def get_tab_category():
    return get_prefs().tab_category


def is_experimental():
    return False
    # return get_prefs().use_experimental


def use_experimental(setting, fallback):
    if not is_experimental():
        return fallback

    prefs = get_prefs()

    return getattr(prefs, setting)
