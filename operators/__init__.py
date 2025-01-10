# Initialize the module
from .set_active_uv_operator import SetActiveUVOperator

def register():
    bpy.utils.register_class(SetActiveUVOperator)

def unregister():
    bpy.utils.unregister_class(SetActiveUVOperator)
