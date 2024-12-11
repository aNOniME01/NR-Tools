# vertex_module.py
import bpy
from .addon_framework import BaseAddonModule

class NinjaToolsVertexModule(BaseAddonModule):
    """Modular Vertex Tools Module"""

    class NinjaToolsDeleteLowVertexObjects(bpy.types.Operator):
        bl_idname = "ninja_tools.delete_low_vertex_objects"
        bl_label = "Delete Low Vertex Objects"
        bl_description = "Delete selected objects with fewer vertices than the specified threshold"
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            vertex_threshold = context.scene.ninja_vertex_threshold
            deleted_count = 0
            objects_to_delete = []

            for obj in context.selected_objects:
                if obj.type == 'MESH':
                    bpy.ops.object.mode_set(mode='OBJECT')
                    vertex_count = len(obj.data.vertices)
                    
                    if vertex_count < vertex_threshold:
                        objects_to_delete.append(obj)

            for obj in objects_to_delete:
                bpy.data.objects.remove(obj, do_unlink=True)
                deleted_count += 1

            self.report({'INFO'}, f"Deleted {deleted_count} object(s) with fewer than {vertex_threshold} vertices")
            
            return {'FINISHED'}

    class NinjaToolsVertexPanel(bpy.types.Panel):
        bl_label = "Ninja Tools - Vertex"
        bl_idname = "VIEW3D_PT_ninja_tools_vertex"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = 'Ninja Tools'
        bl_context = "objectmode"

        def draw(self, context):
            layout = self.layout
            box = layout.box()
            box.label(text="Delete Low Vertex Objects")
            row = box.row()
            row.prop(context.scene, "ninja_vertex_threshold", text="Vertex Threshold")
            row.operator("ninja_tools.delete_low_vertex_objects", text="Delete")

    @classmethod
    def register(cls):
        # Call parent class register method
        super().register()
        
        # Register scene property for vertex threshold
        bpy.types.Scene.ninja_vertex_threshold = bpy.props.IntProperty(
            name="Vertex Threshold", 
            description="Minimum number of vertices to keep an object",
            default=10,
            min=0
        )

    @classmethod
    def unregister(cls):
        # Unregister parent class
        super().unregister()
        
        # Remove scene property
        del bpy.types.Scene.ninja_vertex_threshold
