import bpy

class ViewportPanel(bpy.types.Panel):
    bl_label = "Model Preparation"
    bl_idname = "OBJECT_PT_viewport_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'R6S NR Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Text input field
        layout.prop(scene, "uv_layer_name")

        # Button to execute the operator
        layout.operator("object.set_active_uv_operator", text="Set Active UV").uv_name = scene.uv_layer_name


def register():
    bpy.types.Scene.uv_layer_name = bpy.props.StringProperty(
        name="UV Layer Name",
        description="Name of the UV layer to set as active render",
        default="uv_2",
    )
    bpy.utils.register_class(ViewportPanel)

def unregister():
    del bpy.types.Scene.uv_layer_name
    bpy.utils.unregister_class(ViewportPanel)
