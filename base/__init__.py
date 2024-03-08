from ..util.register import module_register_factory

modules = [
    'preferences',
]

register, unregister = module_register_factory(__name__, modules)
