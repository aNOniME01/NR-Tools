# addon_framework.py
import bpy
import importlib
import os
import inspect

class BaseAddonModule:
    """Base class for creating modular Blender addon components"""
    
    @classmethod
    def register(cls):
        """Register method to be implemented by subclasses"""
        # Automatically register all classes defined in the module
        for name, obj in inspect.getmembers(cls):
            if inspect.isclass(obj) and hasattr(obj, 'bl_idname'):
                try:
                    bpy.utils.register_class(obj)
                except Exception as e:
                    print(f"Error registering {obj.__name__}: {e}")

    @classmethod
    def unregister(cls):
        """Unregister method to be implemented by subclasses"""
        # Automatically unregister all classes defined in the module
        for name, obj in reversed(list(inspect.getmembers(cls))):
            if inspect.isclass(obj) and hasattr(obj, 'bl_idname'):
                try:
                    bpy.utils.unregister_class(obj)
                except Exception as e:
                    print(f"Error unregistering {obj.__name__}: {e}")

class ModularAddonManager:
    """Manages registration of modular addon components"""
    
    @staticmethod
    def load_modules(addon_path):
        """
        Dynamically load all addon modules from the 'modules' subdirectory
        
        :param addon_path: Base path of the addon
        :return: List of loaded module classes
        """
        # Construct the path to the modules folder
        module_path = os.path.join(addon_path, 'modules')
        
        loaded_modules = []
        
        # Ensure the modules path is a directory
        if not os.path.isdir(module_path):
            print(f"Error: {module_path} is not a valid directory")
            return loaded_modules
        
        # Iterate through Python files in the modules directory
        for filename in os.listdir(module_path):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]  # Remove .py extension
                
                try:
                    # Dynamically import the module
                    spec = importlib.util.spec_from_file_location(
                        module_name, 
                        os.path.join(module_path, filename)
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Find and store module classes that inherit from BaseAddonModule
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, BaseAddonModule) and 
                            obj is not BaseAddonModule):
                            loaded_modules.append(obj)
                    
                except Exception as e:
                    print(f"Error loading module {filename}: {e}")
        
        return loaded_modules

    @staticmethod
    def register_modules(modules):
        """
        Register all loaded modules
        
        :param modules: List of module classes to register
        """
        for module in modules:
            try:
                module.register()
                print(f"Registered module: {module.__name__}")
            except Exception as e:
                print(f"Error registering module {module.__name__}: {e}")

    @staticmethod
    def unregister_modules(modules):
        """
        Unregister all loaded modules
        
        :param modules: List of module classes to unregister
        """
        for module in reversed(modules):
            try:
                module.unregister()
                print(f"Unregistered module: {module.__name__}")
            except Exception as e:
                print(f"Error unregistering module {module.__name__}: {e}")