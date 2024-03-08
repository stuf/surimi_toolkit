# Surimi Toolkit

Shorthands to some functions I find myself missing in my day to day Blender work from the comfort of the 3D view (without having to fumblr around in settings panels)

## Features ✨

Things available in the sidebar:

- Toggle _Simplify_ and max subdivs
- Change preview and render max samples settings
- Easily change preview render pixel size
- Quickly rename in-game objects weights to match rigify weights names (**Only when meshes are selected**)
- Quick toggle of pose and rest position for armatures (**Only when armatures are selected**)

## Requirements

- Blender 4.0.0 (probably works on pre-4.0 too)

## Installation

Download this repository as a ZIP file, install in Blender through the "Install" button in the Blender Addon window.

## Things that need doing

### Octane Render

- [ ] Operator: Convert `OctaneRGBImage` node(s) to legacy `ShaderNodeOctImageTex`
- [ ] Shader Editor: Add `Layout` and `Group` menus to the `Add Node` menu

### 3D View

- [ ] Common fixes to an object's modifier stack order (Armature first, Subdivision last)
- [ ] Fix issues with `Knee` and `Elbow` weights
  - [ ] Add (and apply?) `VertexWeightMix` modifier; A=DEF-forearm.L, B=Elbow_L, Vertex Set=All, Mix Mode=Add
- [ ] Ability to easily add character-related properties on rigs (like ink color, skin tone, etc)
- [ ] Toggle for mesh symmetry in the X axis
- [ ] Create empty vertex groups for the opposite side (`Toe_L` -> `Toe_R`, for shoes w/ mirror modifier)
- [ ] Rename vertex groups from one side to the other (rename groups from `_L` to `_R`)

### Codebase

- [ ] Reorganize

### Other ???

- [ ] Make it easier to make a nodegroup or similar that has characer properties for use in nodes (making drivers by hand is boring)

## Acknowledgements

- Floaty64 for giving tons of valuable feedback
- ChaoticPan for volunteering to test this out
- [@ranjian0](https://github.com/ranjian0) for the tool of generating Python module stubs to get editor integration in VS Code Intellisense ([Blender-PyCharm](https://github.com/ranjian0/Blender-PyCharm))
