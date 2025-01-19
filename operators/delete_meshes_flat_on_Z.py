import bpy

class DeletMeshesFlatOnZ(bpy.types.Operator):
    """Delete all flat meshes on Z dimension"""
    bl_idname = "object.delete_meshes_flat_on_z"
    bl_label = "Delete Meshes Flat Meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        count = 0

        bpy.ops.object.select_all(action='DESELECT')
        
        # Loop through visible meshes
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.visible_get():
                # Calculate the dimensions of the object
                dimensions = obj.dimensions
                
                # Check if the Z-dimension is exactly 0
                if dimensions.z == 0:
                    bpy.data.objects.remove(obj) 
                    count += 1
            
            self.report({'INFO'}, f"Deleted {count} mesh objects without materials")
            return {'FINISHED'}

# Register and unregister classes
def register():
    bpy.utils.register_class(DeletMeshesFlatOnZ)


def unregister():
    bpy.utils.unregister_class(DeletMeshesFlatOnZ)
