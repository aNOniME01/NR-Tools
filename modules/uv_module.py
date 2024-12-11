# uv_module.py
import bpy
from .addon_framework import BaseAddonModule

class NinjaToolsUVModule(BaseAddonModule):
    """Modular UV Tools Module"""

    class NinjaToolsSetActiveUV(bpy.types.Operator):
        bl_idname = "ninja_tools.set_active_uv"
        bl_label = "Set Active UV Layer"
        bl_description = "Set the specified UV layer to active render on selected objects"
        bl_options = {'REGISTER', 'UNDO'}

        uv_name: bpy.props.StringProperty(name="UV Name", default="uv_2")

        def execute(self, context):
            uv_name = self.uv_name
            for obj in context.selected_objects:
                if obj.type == 'MESH' and obj.visible_get():
                    if uv_name in obj.data.uv_layers:
                        obj.data.uv_layers[uv_name].active_render = True
                        uv_layer_index = [uv.name for uv in obj.data.uv_layers].index(uv_name)
                        obj.data.uv_layers.active_index = uv_layer_index
                    else:
                        self.report({'WARNING'}, f"UV layer '{uv_name}' not found on object '{obj.name}'")
            
            return {'FINISHED'}

    class NinjaToolsPanel(bpy.types.Panel):
        bl_label = "Ninja Tools - UV"
        bl_idname = "VIEW3D_PT_ninja_tools_uv"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = 'Ninja Tools'
        bl_context = "objectmode"

        def draw(self, context):
            layout = self.layout
            box = layout.box()
            box.label(text="Set Active UV Layer")
            row = box.row()
            row.prop(context.scene, "ninja_uv_name", text="UV Name")
            operator = row.operator("ninja_tools.set_active_uv", text="Apply")
            operator.uv_name = context.scene.ninja_uv_name

    @classmethod
    def register(cls):
        print(f"Attempting to register {cls.__name__}")
        
        # Call parent class register method
        super().register()
        
        # Register scene property for UV name
        bpy.types.Scene.ninja_uv_name = bpy.props.StringProperty(
            name="UV Name", 
            default="uv_2"
        )

    @classmethod
    def unregister(cls):
        # Unregister parent class
        super().unregister()
        
        # Remove scene property
        del bpy.types.Scene.ninja_uv_name
