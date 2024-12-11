import os
import sys
from pathlib import Path

# Add the `modules` directory to Python's path
addon_dir = Path(__file__).parent
modules_dir = addon_dir / "modules"
if str(modules_dir) not in sys.path:
    sys.path.append(str(modules_dir))

import os
import bpy
import importlib
from . import addon_framework

# Addon metadata
bl_info = {
    "name": "Ninja Tools",
    "author": "Nam-Nam",
    "version": (0, 0, 1),
    "blender": (4, 2, 3),
    "location": "View3D > Sidebar > Ninja Tools",
    "description": "Tools for working with UV layers, materials, textures, and vertices",
    "category": "3D View",
}

# Dynamically import all module files
modules = [
    'material_module',
    'texture_module', 
    'uv_module', 
    'vertex_module'
]

loaded_modules = []

def register():
    # Dynamically import and store modules
    for module_name in modules:
        module_path = f".{module_name}"
        try:
            module = importlib.import_module(module_path, package=__name__)
            loaded_modules.append(module)
            print(f"Successfully imported module: {module_name}")
        except Exception as e:
            print(f"Error importing {module_name}: {e}")

    # Register all modules
    for module in loaded_modules:
        for name, obj in module.__dict__.items():
            if hasattr(obj, 'register'):
                try:
                    obj.register()
                    print(f"Registered: {name}")
                except Exception as e:
                    print(f"Error registering {name}: {e}")

def unregister():
    # Unregister modules in reverse order
    for module in reversed(loaded_modules):
        for name, obj in module.__dict__.items():
            if hasattr(obj, 'unregister'):
                try:
                    obj.unregister()
                    print(f"Unregistered: {name}")
                except Exception as e:
                    print(f"Error unregistering {name}: {e}")