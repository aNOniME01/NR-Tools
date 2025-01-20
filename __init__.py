bl_info = {
    "name": "R6S NR Tools",
    "version": (0, 2, 0),
    "blender": (4, 3, 2),
    "category": "Object",
    "author": "Nam-Nam",
    "location": "View3D > Sidebar > R6S NR Tools",
    "description": "Tools For Imported R6S Ninja Ripper Models.",
}

import importlib
import bpy

# Import modules
from .operators import set_active_uv_operator, delete_meshes_without_mat, delete_meshes_flat_on_z, find_missing_textures_for_mat, move_selected_to_gizmo
from .panels import viewport_panel

# Reload for development purposes
modules = [set_active_uv_operator, delete_meshes_without_mat, delete_meshes_flat_on_z, find_missing_textures_for_mat, move_selected_to_gizmo
           , viewport_panel]
for module in modules:
    importlib.reload(module)

# Register and unregister functions
def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
