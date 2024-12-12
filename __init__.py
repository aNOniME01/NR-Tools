bl_info = {
    "name": "Test Addon",
    "author": "Nam-Nam",
    "version": (0, 0, 1),
    "blender": (4, 2, 3),
    "location": "View3D",
    "description": "A simple test addon",
    "category": "Development"
}

import os
import sys
import importlib
import inspect
import bpy

addon_dir = os.path.dirname(__file__)
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

print(addon_dir)

class BaseAddonModule:
    @classmethod
    def register(cls):
        for name, obj in inspect.getmembers(cls):
            if inspect.isclass(obj) and hasattr(obj, 'bl_idname'):
                bpy.utils.register_class(obj)

    @classmethod
    def unregister(cls):
        for name, obj in reversed(list(inspect.getmembers(cls))):
            if inspect.isclass(obj) and hasattr(obj, 'bl_idname'):
                bpy.utils.unregister_class(obj)

def load_modules():
    modules = []
    module_dir = os.path.join(addon_dir, 'modules')
    
    for filename in os.listdir(module_dir):

        

        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'modules.{filename[:-3]}'
            print(f'import filename: {filename}')
            try:
                module = importlib.import_module(module_name)
                
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BaseAddonModule) and 
                        obj is not BaseAddonModule):
                        modules.append(obj)
                
            except Exception as e:
                print(f"Error importing module {filename}: {e}")
    
    return modules

def register():
    global LOADED_MODULES
    LOADED_MODULES = load_modules()
    
    for module in LOADED_MODULES:
        module.register()

def unregister():
    for module in reversed(LOADED_MODULES):
        module.unregister()