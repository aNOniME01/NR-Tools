# Initialize the module
import bpy
from .set_active_uv_operator import SetActiveUVOperator
from .delete_meshes_flat_on_z import DeletMeshesFlatOnZ
from .move_selected_to_gizmo import MoveToGizmoOperator

from .find_missing_textures_for_mat import FindMissingTexturesForNRMaterials

from .delete_meshes_without_mat import DeleteMeshesWithNoMaterials


def register():
    bpy.utils.register_class(SetActiveUVOperator)
    bpy.utils.register_class(DeletMeshesFlatOnZ)
    bpy.utils.register_class(MoveToGizmoOperator)

    bpy.utils.register_class(FindMissingTexturesForNRMaterials)

    bpy.utils.register_class(DeleteMeshesWithNoMaterials)

def unregister():
    bpy.utils.unregister_class(SetActiveUVOperator)
    bpy.utils.unregister_class(DeletMeshesFlatOnZ)
    bpy.utils.unregister_class(MoveToGizmoOperator)

    bpy.utils.unregister_class(FindMissingTexturesForNRMaterials)
    
    bpy.utils.unregister_class(DeleteMeshesWithNoMaterials)
