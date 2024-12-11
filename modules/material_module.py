# material_module.py
import bpy
from .addon_framework import BaseAddonModule

class NinjaToolsMaterialModule(BaseAddonModule):
    """Modular Material Tools Module"""

    class NinjaToolsMergeMaterials(bpy.types.Operator):
        bl_idname = "ninja_tools.merge_materials"
        bl_label = "Merge Materials"
        bl_description = "Merge materials that share the same image textures, ignoring empty image textures"
        bl_options = {'REGISTER', 'UNDO'}

        def get_image_textures_from_material(self, material):
            image_textures = set()
            if material.use_nodes and material.node_tree:
                for node in material.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image is not None:
                        image_textures.add(node.image.name.split('.png')[0])
            return image_textures

        def compare_materials(self, mat1, mat2):
            textures1 = self.get_image_textures_from_material(mat1)
            textures2 = self.get_image_textures_from_material(mat2)
            return textures1 == textures2

        def merge_materials(self, mat_keep, mat_remove):
            print(f"Merged material: {mat_keep.name} (kept), {mat_remove.name} (removed)")
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    for slot in obj.material_slots:
                        if slot.material == mat_remove:
                            slot.material = mat_keep

        def execute(self, context):
            materials = bpy.data.materials
            merged_materials = set()
            checked_materials = set()

            for mat1 in materials:
                if mat1 in merged_materials or not mat1.use_nodes or mat1 in checked_materials:
                    continue

                for mat2 in materials:
                    if mat1 != mat2 and mat2 not in merged_materials and mat2.use_nodes:
                        if self.compare_materials(mat1, mat2):
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

    class NinjaToolsMaterialPanel(bpy.types.Panel):
        bl_label = "Ninja Tools - Materials"
        bl_idname = "VIEW3D_PT_ninja_tools_materials"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = 'Ninja Tools'
        bl_context = "objectmode"

        def draw(self, context):
            layout = self.layout
            box = layout.box()
            box.label(text="Merge Materials Tool")
            box.operator("ninja_tools.merge_materials", text="Merge Materials")
