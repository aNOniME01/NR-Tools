bl_info = {
    "name": "Ninja Ripper Tools",
    "blender": (0, 0, 1),
    "category": "Object",
    "description": "This is an addon developed for Ripping R6S models using Ninja Ripper.",
}

import importlib
import bpy

# Import modules
from .operators import set_active_uv_operator
from .panels import viewport_panel

# Reload for development purposes
modules = [set_active_uv_operator, viewport_panel]
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
