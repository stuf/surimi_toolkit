"""
Proof-of-Concept implementation of creating a nodegroup through Python,
adding most commonly used parameters used for a character.

Meant for easily adding a nodegroup such that a new character can use a unique nodegroup
instead of having to duplicate an existing one.

- TODO: Implement this as an operator
"""
import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D
from enum import Enum
from operator import itemgetter
from dataclasses import dataclass

# Constants

NODEGROUP_NAME = '_Character_Params'


#

class NodeInterface(str, Enum):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'


class SocketType(str, Enum):
    FLOAT = 'NodeSocketFloat'
    COLOR = 'NodeSocketColor'
    VECTOR = 'NodeSocketVector'


class SocketKind(str, Enum):
    IN = 'INPUT'
    OUT = 'OUTPUT'


class NodeType(str, Enum):
    SHADER_NODE_TREE = 'ShaderNodeTree'
    RGB = 'ShaderNodeRGB'
    VALUE = 'ShaderNodeValue'
    GROUP_INPUT = 'NodeGroupInput'
    GROUP_OUTPUT = 'NodeGroupOutput'

#


panels = {
    'Presets': [
        {'name': 'Species',
         'description': '',
         'in_out': SocketKind.OUT,
         'socket_type': SocketType.FLOAT,
         },
    ],
    'Colors': [
        {'name': 'PrimaryColor',
         'description': '',
         'in_out': SocketKind.OUT,
         'socket_type': SocketType.COLOR,
         },
        {'name': 'SecondaryColor',
         'description': '',
         'in_out': SocketKind.OUT,
         'socket_type': SocketType.COLOR,
         },
        {'name': 'SkinTone',
         'description': '',
         'in_out': SocketKind.OUT,
         'socket_type': SocketType.COLOR,
         },
        {'name': 'TransmissionColor',
         'description': '',
         'in_out': SocketKind.OUT,
         'socket_type': SocketType.COLOR,
         }
    ],
    'Values': [
        {'name': 'RghWeight',
         'description': '',
         'in_out': SocketKind.OUT,
         'socket_type': SocketType.FLOAT,
         },
        {'name': 'EmiWeight',
         'description': '',
         'in_out': SocketKind.OUT,
         'socket_type': SocketType.FLOAT,
         },
        {'name': 'TrmWeight',
         'description': '',
         'in_out': SocketKind.OUT,
         'socket_type': SocketType.FLOAT,
         }
    ],
}

nodes = [
    {'name': 'PrimaryColor',
     'type': NodeType.RGB,
     'values': [{'output': 0, 'value': (0.056, 0.105, 0.896, 1.0)}],
     'location': (-200, 0),
     },
    {'name': 'SecondaryColor',
     'type': NodeType.RGB,
     'values': [{'output': 0, 'value': (0.0, 0.0, 0.0, 1.0)}],
     'location': (-200, -200),
     },
    {'name': 'SkinTone',
     'type': NodeType.RGB,
     'values': [{'output': 0, 'value': (0.896, 0.701, 0.701, 1.0)}],
     'location': (-200, -400),
     },
    {'name': 'TransmissionColor',
     'type': NodeType.RGB,
     'values': [{'output': 0, 'value': (0.701, 0.1, 0.1, 1.0)}],
     'location': (-200, -600),
     },
]

links = [
    {'from': {'name': 'PrimaryColor', 'output': 'Color'},
     'to': {'name': 'Output', 'input': 'PrimaryColor'},
     },
    {'from': {'name': 'SecondaryColor', 'output': 'Color'},
     'to': {'name': 'Output', 'input': 'SecondaryColor'},
     },
    {'from': {'name': 'SkinTone', 'output': 'Color'},
     'to': {'name': 'Output', 'input': 'SkinTone'},
     },
    {'from': {'name': 'TransmissionColor', 'output': 'Color'},
     'to': {'name': 'Output', 'input': 'TransmissionColor'},
     },
]


def execute():
    sockets = {}

    if NODEGROUP_NAME in D.node_groups:
        D.node_groups.remove(D.node_groups.get(NODEGROUP_NAME))

    grp = D.node_groups.new(NODEGROUP_NAME, NodeType.SHADER_NODE_TREE)

    for panel_name, panel_sockets in panels.items():
        sockets[panel_name] = []
        panel = grp.interface.new_panel(panel_name)

        # If a panel is empty, bail out of this iteration
        if not len(panel_sockets):
            continue

        # Since we have a panel that should have sockets in it,
        # iterate and create them
        for socket in panel_sockets:
            # If we've done something silly, bail out without doing anything
            if not socket.keys():
                continue

            name, description, in_out, socket_type = itemgetter(
                'name', 'description', 'in_out', 'socket_type')(socket)

            grp.interface.new_socket(
                name,
                description=description,
                in_out=in_out,
                socket_type=socket_type,
                parent=panel,
            )

    # Create group input and output nodes
    g_out = grp.nodes.new(NodeType.GROUP_OUTPUT)
    g_out.name = 'Output'
    g_out.location = (100, 0)
    g_in = grp.nodes.new(NodeType.GROUP_INPUT)
    g_in.location = (-550, 0)

    # Create the nodes themselves
    for panel_name in nodes:
        node_type, name, location, values = itemgetter(
            'type', 'name', 'location', 'values')(panel_name)
        node = grp.nodes.new(node_type)
        node.name = name
        node.label = name
        node.location = location
        for o in values:
            node.outputs[o['output']].default_value = o['value']

    # Link nodes
    for l in links:
        link_from, link_to = itemgetter('from', 'to')(l)
        grp.links.new(grp.nodes[link_from['name']].outputs[link_from['output']],
                      grp.nodes[link_to['name']].inputs[link_to['input']])


#
if __name__ == '__main__':
    execute()
