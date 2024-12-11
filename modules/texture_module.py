# texture_module.py
import bpy
from .addon_framework import BaseAddonModule

class NinjaToolsTextureModule(BaseAddonModule):
    """Modular Texture Tools Module"""

    class NinjaToolsSetTextureNonColor(bpy.types.Operator):
        bl_idname = "ninja_tools.set_texture_non_color"
        bl_label = "Set Selected Texture Nodes to Non-Color"
        bl_description = "Set selected texture nodes' color space to Non-Color"
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            obj = bpy.context.object
            
            if obj is not None and obj.type == 'MESH':
                for mat_slot in obj.material_slots:
                    mat = mat_slot.material
                    
                    if mat is not None and mat.use_nodes:
                        node_tree = mat.node_tree
                        
                        for node in node_tree.nodes:
                            if node.select and node.type == 'TEX_IMAGE':
                                if hasattr(node, 'image') and node.image is not None:
                                    node.image.colorspace_settings.name = 'Non-Color'
                                    print(f"Set '{node.name}' to Non-Color space")
            return {'FINISHED'}

    class NinjaToolsNodeEditorPanel(bpy.types.Panel):
        bl_label = "Ninja Tools - Node Editor"
        bl_idname = "NODE_PT_ninja_tools_texture"
        bl_space_type = 'NODE_EDITOR'
        bl_region_type = 'UI'
        bl_category = 'Ninja Tools'

        def draw(self, context):
            layout = self.layout
            layout.label(text="Texture Tools")
            layout.operator("ninja_tools.set_texture_non_color", text="Set Selected to Non-Color")

    @classmethod
    def register(cls):
        print(f"Attempting to register {cls.__name__}")
        super().register()
        print(f"Successfully registered {cls.__name__}")

    @classmethod
    def unregister(cls):
        print(f"Attempting to unregister {cls.__name__}")
        super().unregister()
        print(f"Successfully unregistered {cls.__name__}")
