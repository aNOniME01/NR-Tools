import bpy

class ViewportPanel(bpy.types.Panel):
    bl_label = "Viewport Panel"
    bl_idname = "viewport_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'R6S NR Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.label(text="Mesh Tools:")
        row = box.row()
        row.operator("object.delete_flat_meshes_on_z", text="Delete Meshes That Have A Flat Z Dimension")
        row = box.row()
        row.operator("object.delete_meshes_without_mat", text="Delete Meshes Without Materials")

        layout.separator()
        
        
        box = layout.box()
        box.label(text="Material Tools:")
        row = box.row()
        row.prop(scene, "uv_layer_name")
        row = box.row()
        row.operator("object.set_active_uv_operator", text="Set Active UV").uv_name = scene.uv_layer_name





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