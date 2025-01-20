import bpy
import bmesh

class ViewportPanel(bpy.types.Panel):
    bl_label = "Viewport Panel"
    bl_idname = "viewport_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'R6S NR Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Main box for mesh tools
        box = layout.box()
        box.label(text="Mesh Tools:")
        row = box.row()
        row.operator("object.delete_meshes_flat_on_z")
        row = box.row()
        row.operator("object.delete_meshes_without_mat")

        # Separate box for "Move to Gizmo" option
        gizmo_box = layout.box()
        gizmo_box.label(text="Alignment Tools:")
        row = gizmo_box.row()

        obj = context.object
        if obj and obj.type == 'MESH':
            # Check if any vertices are selected
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            selected_verts = any(v.select for v in bm.verts)
            bm.free()

            if not selected_verts:
                gizmo_box.label(text="No vertices selected.", icon='ERROR')

            # Enable button only if there are selected vertices
            row = gizmo_box.row()
            row.enabled = selected_verts
            row.operator("object.move_selected_to_gizmo", text="Move to Gizmo")
        else:
            gizmo_box.label(text="Select a valid mesh object.", icon='ERROR')


        box = layout.box()
        box.label(text="Find Missing Textures For Selected:")
        row = box.row()
        settings = context.scene.texture_import_settings
        row = box.row()
        row.prop(settings, "log_file_path")
        row = box.row()
        row.prop(settings, "texture_folder")
        row = box.row()
        row.operator("texture.find_missing_textures_for_mat")


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

    bpy.utils.register_class(ViewportPanel)

    bpy.utils.register_class(TextureImportSettings)

    bpy.types.Scene.texture_import_settings = bpy.props.PointerProperty(type=TextureImportSettings)
    bpy.types.Scene.uv_layer_name = bpy.props.StringProperty(
        name="UV Layer Name",
        description="Name of the UV layer to set as active render",
        default="uv_2",
    )

def unregister():
    bpy.utils.unregister_class(ViewportPanel)

    bpy.utils.unregister_class(TextureImportSettings)
    
    del bpy.types.Scene.texture_import_settings
    del bpy.types.Scene.uv_layer_name