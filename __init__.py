# __init__.py
import os
import bpy
from . import addon_framework

bl_info = {
    "name": "Ninja Tools",
    "blender": (4, 2, 3),
    "category": "3D View",
    "description": "Tools for working with UV layers, focusing on active render and setting UV layers, and merging materials.",
    "version": (0, 0, 1),
    "author": "Nam-Nam"
}

# Get the absolute path of the addon directory
addon_path = os.path.dirname(os.path.abspath(__file__))

def register():
    """Register the addon modules"""
    # Load all modules from the 'modules' directory
    loaded_modules = addon_framework.ModularAddonManager.load_modules(addon_path)
    
    # Register all loaded modules
    addon_framework.ModularAddonManager.register_modules(loaded_modules)

def unregister():
    """Unregister the addon modules"""
    # Load all modules again to unregister them
    loaded_modules = addon_framework.ModularAddonManager.load_modules(addon_path)
    
    # Unregister all loaded modules
    addon_framework.ModularAddonManager.unregister_modules(loaded_modules)