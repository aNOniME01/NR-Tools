import bpy

class DeleteMeshesWithNoMaterials(bpy.types.Operator):
    """Delete all mesh objects without materials"""
    bl_idname = "object.delete_meshes_without_mat"
    bl_label = "Delete Meshes Without Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Loop through all objects in the scene
        for obj in bpy.context.scene.objects:
            # Check if the object is a mesh and has no materials
            if obj.type == 'MESH':
                if not obj.data.materials:  # If there are no materials attached
                    bpy.data.objects.remove(obj)  # Delete the object
        self.report({'INFO'}, "Deleted all mesh objects without materials")
        return {'FINISHED'}

# Register and unregister classes
def register():
    bpy.utils.register_class(DeleteMeshesWithNoMaterials)


def unregister():
    bpy.utils.unregister_class(DeleteMeshesWithNoMaterials)
