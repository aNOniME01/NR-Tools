bl_info = {
    "name": "Ninja Tools",
    "blender": (2, 80, 0),
    "category": "3D View",
    "description": "Tools for working with UV layers, focusing on active render and setting UV layers, and merging materials.",
    "version": (1, 1, 0),
    "author": "Your Name",
    "location": "View3D > Sidebar > Ninja Tools",
}

import bpy

# Define an operator class that performs the UV layer actions
class NinjaToolsSetActiveUV(bpy.types.Operator):
    bl_idname = "ninja_tools.set_active_uv"
    bl_label = "Set Active UV Layer"
    bl_description = "Set the specified UV layer to active render on selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    # Create a string property for the UV name input
    uv_name: bpy.props.StringProperty(name="UV Name", default="uv_2")

    def execute(self, context):
        uv_name = self.uv_name  # Use the value from the operator's property to ensure consistency
        # Loop through selected objects in the scene
        for obj in context.selected_objects:
            # Check if the object is a mesh and visible in the viewport
            if obj.type == 'MESH' and obj.visible_get():
                # Ensure the object has the specified UV layer
                if uv_name in obj.data.uv_layers:
                    # Set active_render to True for the specified UV layer
                    obj.data.uv_layers[uv_name].active_render = True

                    # Set the active UV map index to the specified UV name if possible
                    uv_layer_index = [uv.name for uv in obj.data.uv_layers].index(uv_name)
                    obj.data.uv_layers.active_index = uv_layer_index
                else:
                    self.report({'WARNING'}, f"UV layer '{uv_name}' not found on object '{obj.name}'")
        
        return {'FINISHED'}

# Define an operator class for merging materials
class NinjaToolsMergeMaterials(bpy.types.Operator):
    bl_idname = "ninja_tools.merge_materials"
    bl_label = "Merge Materials"
    bl_description = "Merge materials that share the same image textures, ignoring empty image textures"
    bl_options = {'REGISTER', 'UNDO'}

    def get_image_textures_from_material(self, material):
        """Get all image texture nodes used in a material"""
        image_textures = set()
        # Ensure the material has a node tree
        if material.use_nodes and material.node_tree:
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image is not None:
                    image_textures.add(node.image.name.split('.png')[0])
        return image_textures

    def compare_materials(self, mat1, mat2):
        """Check if two materials use the same image textures"""
        textures1 = self.get_image_textures_from_material(mat1)
        textures2 = self.get_image_textures_from_material(mat2)
        return textures1 == textures2

    def merge_materials(self, mat_keep, mat_remove):
        """Merge materials by replacing all instances of mat_remove with mat_keep, then delete mat_remove"""
        # Update all meshes that use the material to use the new one
        print(f"Merged material: {mat_keep.name} (kept), {mat_remove.name} (removed)")
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material == mat_remove:
                        slot.material = mat_keep

    def execute(self, context):
        # Get all materials in the scene
        materials = bpy.data.materials
        merged_materials = set()  # To track merged materials
        checked_materials = set()  # To track materials that have already been compared

        # Loop over materials to compare them
        for mat1 in materials:
            # Skip if already merged or not using nodes
            if mat1 in merged_materials or not mat1.use_nodes or mat1 in checked_materials:
                continue

            for mat2 in materials:
                # Ensure mat2 has not been checked or merged
                if mat1 != mat2 and mat2 not in merged_materials and mat2.use_nodes:
                    if self.compare_materials(mat1, mat2):
                        # If they have the same image textures, keep the one with more nodes
                        if len(mat1.node_tree.nodes) >= len(mat2.node_tree.nodes):
                            self.merge_materials(mat1, mat2)
                            merged_materials.add(mat2)
                        else:
                            self.merge_materials(mat2, mat1)
                            merged_materials.add(mat1)
                            break

            checked_materials.add(mat1)

        for rem_mat in merged_materials:
            bpy.data.materials.remove(rem_mat)

        return {'FINISHED'}

# Define an operator class to set selected texture nodes to Non-Color space
class NinjaToolsSetTextureNonColor(bpy.types.Operator):
    bl_idname = "ninja_tools.set_texture_non_color"
    bl_label = "Set Selected Texture Nodes to Non-Color"
    bl_description = "Set selected texture nodes' color space to Non-Color"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the current active object
        obj = bpy.context.object
        
        # Ensure there's an active object and it has material slots
        if obj is not None and obj.type == 'MESH':
            for mat_slot in obj.material_slots:
                mat = mat_slot.material
                
                # Ensure the material uses nodes
                if mat is not None and mat.use_nodes:
                    node_tree = mat.node_tree
                    
                    # Iterate over selected nodes in the node tree
                    for node in node_tree.nodes:
                        if node.select and node.type == 'TEX_IMAGE':
                            # Set color space to Non-Color if the node is a texture node
                            if hasattr(node, 'image') and node.image is not None:
                                node.image.colorspace_settings.name = 'Non-Color'
                                print(f"Set '{node.name}' to Non-Color space")
        return {'FINISHED'}

# New operator for deleting low-vertex objects
class NinjaToolsDeleteLowVertexObjects(bpy.types.Operator):
    bl_idname = "ninja_tools.delete_low_vertex_objects"
    bl_label = "Delete Low Vertex Objects"
    bl_description = "Delete selected objects with fewer vertices than the specified threshold"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        vertex_threshold = context.scene.ninja_vertex_threshold
        deleted_count = 0

        # Temporary list to avoid modifying selection during iteration
        objects_to_delete = []

        for obj in context.selected_objects:
            if obj.type == 'MESH':
                # Ensure we're in object mode to get vertex count
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Count vertices
                vertex_count = len(obj.data.vertices)
                
                if vertex_count < vertex_threshold:
                    objects_to_delete.append(obj)

        # Delete identified objects
        for obj in objects_to_delete:
            bpy.data.objects.remove(obj, do_unlink=True)
            deleted_count += 1

        # Report the number of deleted objects
        self.report({'INFO'}, f"Deleted {deleted_count} object(s) with fewer than {vertex_threshold} vertices")
        
        return {'FINISHED'}

# Define a panel class to add UI elements to the Node Editor sidebar
class NinjaToolsNodeEditorPanel(bpy.types.Panel):
    bl_label = "Ninja Tools - Node Editor"
    bl_idname = "NODE_PT_ninja_tools"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Ninja Tools'

    def draw(self, context):
        layout = self.layout
        # Add Set Texture to Non-Color tool
        layout.label(text="Texture Tools")
        layout.operator("ninja_tools.set_texture_non_color", text="Set Selected to Non-Color")

# Define a panel class to add UI elements to the 3D view sidebar
class NinjaToolsPanel(bpy.types.Panel):
    bl_label = "Ninja Tools"
    bl_idname = "VIEW3D_PT_ninja_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Ninja Tools'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        
        # UV Layer Box
        box = layout.box()
        box.label(text="Set Active UV Layer")
        row = box.row()
        row.prop(context.scene, "ninja_uv_name", text="UV Name")
        operator = row.operator("ninja_tools.set_active_uv", text="Apply")
        operator.uv_name = context.scene.ninja_uv_name

        # Merge Materials Box
        box = layout.box()
        box.label(text="Merge Materials Tool")
        box.operator("ninja_tools.merge_materials", text="Merge Materials")

        # Low Vertex Object Deletion Box
        box = layout.box()
        box.label(text="Delete Low Vertex Objects")
        row = box.row()
        row.prop(context.scene, "ninja_vertex_threshold", text="Vertex Threshold")
        row.operator("ninja_tools.delete_low_vertex_objects", text="Delete")

# Register the add-on
classes = [
    NinjaToolsSetActiveUV,
    NinjaToolsMergeMaterials,
    NinjaToolsSetTextureNonColor,
    NinjaToolsNodeEditorPanel,
    NinjaToolsPanel,
    NinjaToolsDeleteLowVertexObjects,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register scene properties
    bpy.types.Scene.ninja_uv_name = bpy.props.StringProperty(name="UV Name", default="uv_2")
    bpy.types.Scene.ninja_vertex_threshold = bpy.props.IntProperty(
        name="Vertex Threshold", 
        description="Minimum number of vertices to keep an object",
        default=10,
        min=0
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Remove properties
    del bpy.types.Scene.ninja_uv_name
    del bpy.types.Scene.ninja_vertex_threshold

if __name__ == "__main__":
    register()
