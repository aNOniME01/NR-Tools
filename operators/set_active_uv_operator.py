import bpy

class SetActiveUVOperator(bpy.types.Operator):
    bl_idname = "object.set_active_uv_operator"
    bl_label = "Set Active UV"
    bl_description = "Set specified UV layer as active render and set UV index to 2"
    bl_options = {'REGISTER', 'UNDO'}

    uv_name: bpy.props.StringProperty(
        name="UV Layer Name",
        description="Name of the UV layer to set as active render",
        default="uv_2",
    )

    def execute(self, context):
        uv_name = self.uv_name

        # Loop through all objects in the scene
        for obj in context.selected_objects:
            # Check if the object is a mesh and visible in the viewport
            if obj.type == 'MESH' and obj.visible_get():
                # Ensure the object has the specified UV layer
                if uv_name in obj.data.uv_layers:
                    # Set active_render to True for the UV layer
                    obj.data.uv_layers[uv_name].active_render = True
                    
                    # Set the active UV map index to 2 (ensure it exists)
                    if len(obj.data.uv_layers) > 2:  # Check if there are at least 3 UV layers
                        obj.data.uv_layers.active_index = 2  # Set the active UV map index to 2

        self.report({'INFO'}, f"UV settings updated for '{uv_name}' on visible mesh objects.")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SetActiveUVOperator)

def unregister():
    bpy.utils.unregister_class(SetActiveUVOperator)