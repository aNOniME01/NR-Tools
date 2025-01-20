import bpy
import os

class FindMissingTexturesForNRMaterials(bpy.types.Operator):
    """Find missing textures for materials form nr log file"""
    bl_idname = "texture.find_missing_textures_for_mat"
    bl_label = "Find Missing Textures For Selected Objects From NR Log File"
    
    def execute(self, context):
        settings = context.scene.texture_import_settings
        log_file_path = settings.log_file_path
        texture_folder = settings.texture_folder

        def get_textures_for_object(log_file_path, texture_folder, object_name):
            """
            Extracts all texture names associated with the given object in the log file.
            """
            # Normalize paths for comparison
            normalized_texture_folder = os.path.normpath(texture_folder)
            object_name_base = object_name.split('.')[0]  # Use only the first part before '.'

            with open(log_file_path, "r") as log_file:
                lines = log_file.readlines()

            # Locate the section for the specific object
            relevant_textures = []
            section_found = False
            start_index = -1

            # Find the section
            for idx, line in enumerate(lines):
                if normalized_texture_folder in line and object_name_base in line:
                    section_found = True
                    start_index = idx
                    break

            if not section_found:
                return []  # No relevant section found

            # Search upward from the starting point
            for i in range(start_index - 1, -1, -1):
                if "---Gathered textures---" in lines[i]:
                    break
                if "File=" in lines[i]:
                    texture_name = lines[i].split("File=")[1].split(".")[0]
                    relevant_textures.append(texture_name)

            # Search downward from the starting point
            for i in range(start_index + 1, len(lines)):
                if "---Gathered textures---" in lines[i]:
                    break
                if "File=" in lines[i]:
                    texture_name = lines[i].split("File=")[1].split(".")[0]
                    relevant_textures.append(texture_name)

            return list(set(relevant_textures))

        def ensure_textures_in_material(material, missing_textures, texture_folder):
            """
            Ensures missing textures are added as image texture nodes to the material.
            """
            if not material.use_nodes:
                material.use_nodes = True

            nodes = material.node_tree.nodes
            existing_texture_names = [
                node.image.name.split(".")[0] for node in nodes if node.type == "TEX_IMAGE" and node.image
            ]

            for tex_name in missing_textures:
                if tex_name not in existing_texture_names:
                    texture_path = os.path.join(texture_folder, tex_name + ".png")
                    if os.path.exists(texture_path):
                        # Ensure the texture is imported into Blender
                        img = bpy.data.images.load(texture_path) if tex_name not in bpy.data.images else bpy.data.images[tex_name]

                        # Add a new image texture node to the material
                        tex_node = nodes.new("ShaderNodeTexImage")
                        tex_node.image = img

        # Iterate over selected objects
        for obj in bpy.context.selected_objects:
            if obj.type == "MESH":
                for mat_slot in obj.material_slots:
                    mat = mat_slot.material
                    if not mat:
                        continue

                    # Gather object name and textures
                    object_name = obj.name.split('.')[0]  # Use only the first part before '.'
                    textures_from_log = get_textures_for_object(log_file_path, texture_folder, object_name)

                    # Ensure textures are added to the material
                    ensure_textures_in_material(mat, textures_from_log, texture_folder)

        self.report({'INFO'}, "Textures from log file appended.")
        return {'FINISHED'}

# Register and unregister classes
def register():
    bpy.utils.register_class(FindMissingTexturesForNRMaterials)


def unregister():
    bpy.utils.unregister_class(FindMissingTexturesForNRMaterials)