import bpy

from .register import get_name


def get_prefs():
    return bpy.context.preferences.addons[get_name()].preferences


def is_experimental():
    return get_prefs().use_experimental


def use_experimental(setting, fallback):
    if not is_experimental():
        return fallback

    prefs = get_prefs()

    return getattr(prefs, setting)
