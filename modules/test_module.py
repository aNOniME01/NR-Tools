import bpy
from __init__ import BaseAddonModule

class TestModule(BaseAddonModule):
    class OBJECT_OT_test_message(bpy.types.Operator):
        """Display a test message"""
        bl_idname = "test_addon.show_message"
        bl_label = "Test Message"
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            self.report({'INFO'}, "Test addon button was pressed!")
            return {'FINISHED'}

    class VIEW3D_PT_test_panel(bpy.types.Panel):
        """Creates a Panel in the 3D Viewport"""
        bl_label = "Test Addon"
        bl_idname = "VIEW3D_PT_test_panel"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = 'Test Addon'

        def draw(self, context):
            layout = self.layout
            layout.operator("test_addon.show_message", text="Test Button")