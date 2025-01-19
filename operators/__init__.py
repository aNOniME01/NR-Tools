# Initialize the module
from .set_active_uv_operator import SetActiveUVOperator
from .delete_meshes_without_mat import DeleteMeshesWithNoMaterials
from .delete_meshes_flat_on_Z import DeletMeshesFlatOnZ

def register():
    bpy.utils.register_class(SetActiveUVOperator)
    bpy.utils.register_class(DeleteMeshesWithNoMaterials)
    bpy.utils.register_class(DeletMeshesFlatOnZ)

def unregister():
    bpy.utils.unregister_class(SetActiveUVOperator)
    bpy.utils.unregister_class(DeleteMeshesWithNoMaterials)
    bpy.utils.unregister_class(DeletMeshesFlatOnZ)
