import bpy
from utilities.text_number_utils import adjust_text_number

class ViewportPanel(bpy.types.Panel):
    bl_label = "Model Preparation"
    bl_idname = "OBJECT_PT_viewport_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'R6S NR Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Row for text property with increment and decrement buttons
        row = layout.row(align=True)
        row.prop(scene, "uv_layer_name", text="")

        # Decrement button
        decrement_button = row.operator("wm.context_set_string", text="-")
        decrement_button.data_path = "scene.uv_layer_name"
        decrement_button.value = adjust_text_number(scene.uv_layer_name, -1, "uv_")

        # Increment button
        increment_button = row.operator("wm.context_set_string", text="+")
        increment_button.data_path = "scene.uv_layer_name"
        increment_button.value = adjust_text_number(scene.uv_layer_name, 1, "uv_")


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
