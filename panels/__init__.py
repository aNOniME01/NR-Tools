import bpy
from .viewport_panel import ViewportPanel

def register():
    bpy.utils.register_class(ViewportPanel)

def unregister():
    bpy.utils.unregister_class(ViewportPanel)
