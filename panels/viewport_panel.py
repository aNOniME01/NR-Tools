import bpy # type: ignore

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
        row.operator("object.delete_meshes_flat_on_z", text="Delete Meshes That Have A Flat Z Dimension")
        row = box.row()
        row.operator("object.delete_meshes_without_mat", text="Delete Meshes Without Materials")


        box = layout.box()
        box.label(text="Find Missing Textures:")
        row = box.row()
        settings = context.scene.texture_import_settings
        layout.prop(settings, "log_file_path")
        layout.prop(settings, "texture_folder")
        layout.operator("texture.add_specific_textures")


        box = layout.box()
        box.label(text="Material Tools:")
        row = box.row()
        row.prop(scene, "uv_layer_name")
        row = box.row()
        row.operator("object.set_active_uv_operator", text="Set Active UV").uv_name = scene.uv_layer_name


class TextureImportSettings(bpy.types.PropertyGroup):
    log_file_path: bpy.props.StringProperty(
        name="Log File Path",
        description="Path to the log file",
        subtype='FILE_PATH',
        default=""
    ) # type: ignore

    texture_folder: bpy.props.StringProperty(
        name="Texture Folder",
        description="Path to the folder containing textures",
        subtype='DIR_PATH',
        default=""
    ) # type: ignore



def register():
    bpy.types.Scene.uv_layer_name = bpy.props.StringProperty(
        name="UV Layer Name",
        description="Name of the UV layer to set as active render",
        default="uv_2",
    )
    bpy.utils.register_class(ViewportPanel)
    
    bpy.utils.register_class(TextureImportSettings)
    bpy.types.Scene.texture_import_settings = bpy.props.PointerProperty(type=TextureImportSettings)

def unregister():
    del bpy.types.Scene.uv_layer_name
    bpy.utils.unregister_class(ViewportPanel)
    
    bpy.utils.unregister_class(TextureImportSettings)
    del bpy.types.Scene.texture_import_settings