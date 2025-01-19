# Initialize the module
from .set_active_uv_operator import SetActiveUVOperator
from .delete_meshes_without_mat import DeleteMeshesWithNoMaterials

def register():
    bpy.utils.register_class(SetActiveUVOperator)
    bpy.utils.register_class(DeleteMeshesWithNoMaterials)

def unregister():
    bpy.utils.unregister_class(SetActiveUVOperator)
    bpy.utils.unregister_class(DeleteMeshesWithNoMaterials)
