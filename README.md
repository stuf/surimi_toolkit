# Surimi Toolkit

Shorthands to some functions I find myself missing in my day to day Blender work from the comfort of the 3D view (without having to fumblr around in settings panels)

- [Features ✨](#features-)
- [Requirements](#requirements)
- [Installation](#installation)
- [Acknowledgements](#acknowledgements)
- [Things that need doing](#things-that-need-doing)
  - [Operators](#operators)
  - [Octane Render](#octane-render)
  - [Cycles](#cycles)
  - [3D View](#3d-view)
  - [Codebase](#codebase)
  - [Other ???](#other-)

## Features ✨

Things available in the sidebar:

- Toggle _Simplify_ and max subdivs
- Change preview and render max samples settings
- Easily change preview render pixel size
- Quickly rename in-game objects weights to match rigify weights names (**Only when meshes are selected**)
- Quick toggle of pose and rest position for armatures (**Only when armatures are selected**)

## Requirements

- Blender 4.0

## Installation

Download this repository as a ZIP file, install in Blender through the "Install" button in the Blender Addon window.

## Acknowledgements

- Floaty64 for giving tons of valuable feedback
- ChaoticPan for volunteering to test this out
- [@ranjian0](https://github.com/ranjian0) for the tool of generating Python module stubs to get editor integration in VS Code Intellisense ([Blender-PyCharm](https://github.com/ranjian0/Blender-PyCharm))

---

## Things that need doing

Disregard anything from this point onward unless you're curious about development progress and whatever.

### Operators

Implement operators out of these scripts:

- [ ] `scripts/rename_rig.py` Given the naming scheme `TYPE-identifier-rest`, rename the `identifier` part of selected (or all) data-blocks matching it.
  - Examples: rename `thing` to `cappy`; `GEO-thing-face` → `GEO-cappy-face`
- [ ] `scripts/make_param_nodegroup.py` Create a predefined nodegroup that's used for common character parameters in materials; ink color, skin tone, skin material density, roughness weight, etc.
- [ ] `scripts/make_ref_environment.py` Create a predefined setup consisting of a camera and a world data-block to make lighting and viewport consistent
- [ ] `scripts/set_render_output.py` I'm lazy, just set the render output to be 16-bit TIFF by default
- [x] ~~`scripts/con_rename_images.py`~~ Handled in `na_selected_nodes`
- [ ] `scripts/na_selected_nodes.py` Given the selected texture image nodes, rename and relabel the images used that match the current material name

### Octane Render

- [ ] Operator: Convert `OctaneRGBImage` node(s) to legacy `ShaderNodeOctImageTex`
- ~~[x] Shader Editor: Add `Layout` and `Group` menus to the `Add Node` menu~~
  - Already fixed in BlenderOctane
- [ ] Enable denoiser for rendering

### Cycles

- [ ] Allow fast switching of preview render's pixel size

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
