bl_info = {
    "name": "Node Group Library Manager",
    "author": "Clay MacDonald",
    "version": (1, 1, 0),
    "blender": (3, 0, 0),
    "location": "Shader Editor & Compositor > N-Panel > Node Library",
    "description": "Manage and version control your node groups with a professional library system",
    "category": "Node",
}

import bpy
import json
import os
from datetime import datetime
from pathlib import Path
import shutil

# Preferences
class NODELIB_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    library_path: bpy.props.StringProperty(
        name="Library Path",
        description="Custom path for node library storage. Leave empty for default location",
        default="",
        subtype='DIR_PATH'
    )
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Node Library Settings:", icon='PREFERENCES')
        
        box = layout.box()
        box.prop(self, "library_path")
        
        row = box.row()
        row.label(text="Current Location:", icon='FILE_FOLDER')
        row.label(text=str(get_library_path()))
        
        row = box.row()
        row.operator("nodelib.open_library_folder", icon='FOLDER_REDIRECT')
        row.operator("nodelib.export_library", icon='EXPORT')
        row.operator("nodelib.import_library", icon='IMPORT')

# Utility functions
def get_library_path():
    prefs = bpy.context.preferences.addons.get(__name__)
    if prefs and prefs.preferences.library_path:
        path = Path(prefs.preferences.library_path)
    else:
        path = Path(bpy.utils.user_resource('SCRIPTS', path="addons")) / "node_library_data"
    
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_library_file():
    return get_library_path() / "library.json"

def get_blends_path():
    path = get_library_path() / "node_groups"
    path.mkdir(exist_ok=True)
    return path

def load_library():
    lib_file = get_library_file()
    if lib_file.exists():
        with open(lib_file, 'r') as f:
            return json.load(f)
    return {"node_groups": [], "tags": []}

def save_library(data):
    with open(get_library_file(), 'w') as f:
        json.dump(data, f, indent=2)

def get_selected_node_group(context):
    """Get the node group from the currently selected node group node"""
    space = context.space_data
    if not space or space.type != 'NODE_EDITOR':
        return None
    
    node_tree = space.edit_tree
    if not node_tree:
        return None
    
    active_node = node_tree.nodes.active
    if not active_node:
        return None
    
    if hasattr(active_node, 'node_tree') and active_node.node_tree:
        return active_node.node_tree
    
    return None

def format_timestamp(iso_string):
    """Format ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%b %d, %Y %I:%M %p")
    except:
        return iso_string

# Operators
class NODELIB_OT_AddToLibrary(bpy.types.Operator):
    bl_idname = "nodelib.add_to_library"
    bl_label = "Add to Library"
    bl_description = "Save selected node group to library with version notes"
    
    notes: bpy.props.StringProperty(
        name="Version Notes",
        description="Describe what changed in this version",
        default=""
    )
    
    tags: bpy.props.StringProperty(
        name="Tags",
        description="Comma-separated tags (e.g., metal, procedural, pbr)",
        default=""
    )
    
    def invoke(self, context, event):
        node_tree = get_selected_node_group(context)
        if node_tree:
            # Load existing tags if this is an update
            library = load_library()
            existing = next((ng for ng in library["node_groups"] if ng["name"] == node_tree.name), None)
            if existing and existing.get("tags"):
                self.tags = ", ".join(existing["tags"])
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "notes")
        layout.prop(self, "tags")
    
    def execute(self, context):
        node_tree = get_selected_node_group(context)
        
        if not node_tree:
            self.report({'ERROR'}, "No node group selected")
            return {'CANCELLED'}
        
        library = load_library()
        existing = next((ng for ng in library["node_groups"] if ng["name"] == node_tree.name), None)
        
        timestamp = datetime.now().isoformat()
        version_num = 1
        
        # Process tags
        tag_list = [t.strip() for t in self.tags.split(",") if t.strip()]
        
        if existing:
            version_num = existing["latest_version"] + 1
            existing["latest_version"] = version_num
            existing["tags"] = tag_list
            existing["versions"].append({
                "version": version_num,
                "timestamp": timestamp,
                "notes": self.notes
            })
        else:
            entry = {
                "name": node_tree.name,
                "type": node_tree.bl_idname,
                "latest_version": version_num,
                "tags": tag_list,
                "versions": [{
                    "version": version_num,
                    "timestamp": timestamp,
                    "notes": self.notes
                }]
            }
            library["node_groups"].append(entry)
        
        # Save node group
        blend_name = f"{node_tree.name}_v{version_num}.blend"
        blend_path = get_blends_path() / blend_name
        bpy.data.libraries.write(str(blend_path), {node_tree}, fake_user=True)
        
        save_library(library)
        
        self.report({'INFO'}, f"✓ Added {node_tree.name} v{version_num} to library")
        return {'FINISHED'}

class NODELIB_OT_AddNodeFromLibrary(bpy.types.Operator):
    """Click to add this node group to your editor"""
    bl_idname = "nodelib.add_node_from_library"
    bl_label = "Add Node"
    
    node_name: bpy.props.StringProperty()
    version: bpy.props.IntProperty(default=-1)
    
    def execute(self, context):
        library = load_library()
        entry = next((ng for ng in library["node_groups"] if ng["name"] == self.node_name), None)
        
        if not entry:
            return {'CANCELLED'}
        
        version = self.version if self.version > 0 else entry["latest_version"]
        blend_name = f"{self.node_name}_v{version}.blend"
        blend_path = get_blends_path() / blend_name
        
        if not blend_path.exists():
            self.report({'ERROR'}, f"File not found: {blend_name}")
            return {'CANCELLED'}
        
        # Check if already imported
        imported_group = bpy.data.node_groups.get(self.node_name)
        
        if not imported_group:
            with bpy.data.libraries.load(str(blend_path), link=False) as (data_from, data_to):
                data_to.node_groups = [self.node_name]
            imported_group = bpy.data.node_groups.get(self.node_name)
        
        if imported_group and context.space_data.type == 'NODE_EDITOR':
            node_tree = context.space_data.edit_tree
            if node_tree:
                if entry["type"] == 'ShaderNodeTree':
                    node = node_tree.nodes.new('ShaderNodeGroup')
                elif entry["type"] == 'CompositorNodeTree':
                    node = node_tree.nodes.new('CompositorNodeGroup')
                elif entry["type"] == 'GeometryNodeTree':
                    node = node_tree.nodes.new('GeometryNodeGroup')
                else:
                    node = node_tree.nodes.new('NodeGroup')
                
                node.node_tree = imported_group
                node.location = context.space_data.cursor_location
                node.select = True
                node_tree.nodes.active = node
                
                self.report({'INFO'}, f"✓ Added {self.node_name} v{version}")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        self.execute(context)
        return {'FINISHED'}

class NODELIB_OT_DeleteFromLibrary(bpy.types.Operator):
    bl_idname = "nodelib.delete_from_library"
    bl_label = "Delete Node Group"
    bl_description = "Delete this entire node group and all versions from library"
    bl_options = {'INTERNAL'}
    
    node_name: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
    
    def execute(self, context):
        library = load_library()
        entry = next((ng for ng in library["node_groups"] if ng["name"] == self.node_name), None)
        
        if entry:
            for version_info in entry["versions"]:
                blend_name = f"{self.node_name}_v{version_info['version']}.blend"
                blend_path = get_blends_path() / blend_name
                if blend_path.exists():
                    blend_path.unlink()
            
            library["node_groups"].remove(entry)
            save_library(library)
            self.report({'INFO'}, f"✓ Deleted {self.node_name} from library")
        
        return {'FINISHED'}

class NODELIB_OT_DeleteVersion(bpy.types.Operator):
    bl_idname = "nodelib.delete_version"
    bl_label = "Delete Version"
    bl_description = "Delete this specific version"
    bl_options = {'INTERNAL'}
    
    node_name: bpy.props.StringProperty()
    version: bpy.props.IntProperty()
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
    
    def execute(self, context):
        library = load_library()
        entry = next((ng for ng in library["node_groups"] if ng["name"] == self.node_name), None)
        
        if not entry:
            return {'CANCELLED'}
        
        version_info = next((v for v in entry["versions"] if v["version"] == self.version), None)
        if not version_info:
            return {'CANCELLED'}
        
        blend_name = f"{self.node_name}_v{self.version}.blend"
        blend_path = get_blends_path() / blend_name
        if blend_path.exists():
            blend_path.unlink()
        
        entry["versions"].remove(version_info)
        
        if not entry["versions"]:
            library["node_groups"].remove(entry)
            self.report({'INFO'}, f"✓ Deleted last version - removed {self.node_name}")
        else:
            if self.version == entry["latest_version"]:
                entry["latest_version"] = max(v["version"] for v in entry["versions"])
            self.report({'INFO'}, f"✓ Deleted {self.node_name} v{self.version}")
        
        save_library(library)
        return {'FINISHED'}

class NODELIB_OT_RefreshLibrary(bpy.types.Operator):
    bl_idname = "nodelib.refresh_library"
    bl_label = "Refresh"
    bl_description = "Refresh library list"
    
    def execute(self, context):
        context.area.tag_redraw()
        return {'FINISHED'}

class NODELIB_OT_OpenLibraryFolder(bpy.types.Operator):
    bl_idname = "nodelib.open_library_folder"
    bl_label = "Open Library Folder"
    bl_description = "Open the library folder in your file browser"
    
    def execute(self, context):
        import subprocess
        import platform
        
        path = str(get_library_path())
        
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        
        return {'FINISHED'}

class NODELIB_OT_ExportLibrary(bpy.types.Operator):
    bl_idname = "nodelib.export_library"
    bl_label = "Export Library"
    bl_description = "Export entire library as a zip file for backup or sharing"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    def invoke(self, context, event):
        self.filepath = "node_library_backup.zip"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        import zipfile
        
        library_path = get_library_path()
        
        with zipfile.ZipFile(self.filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(library_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(library_path)
                    zipf.write(file_path, arcname)
        
        self.report({'INFO'}, f"✓ Library exported to {self.filepath}")
        return {'FINISHED'}

class NODELIB_OT_ImportLibrary(bpy.types.Operator):
    bl_idname = "nodelib.import_library"
    bl_label = "Import Library"
    bl_description = "Import a library from a zip file (merges with existing)"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        import zipfile
        
        library_path = get_library_path()
        
        with zipfile.ZipFile(self.filepath, 'r') as zipf:
            zipf.extractall(library_path)
        
        self.report({'INFO'}, "✓ Library imported successfully")
        return {'FINISHED'}

# UI Panel
class NODELIB_PT_LibraryPanel(bpy.types.Panel):
    bl_label = "Node Library"
    bl_idname = "NODELIB_PT_library_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Node Library"
    
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in {'ShaderNodeTree', 'CompositorNodeTree', 'GeometryNodeTree'}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Header with save current
        box = layout.box()
        col = box.column(align=True)
        
        node_tree = get_selected_node_group(context)
        if node_tree:
            row = col.row(align=True)
            row.label(text=node_tree.name, icon='NODETREE')
            row.operator("nodelib.add_to_library", text="Save", icon='EXPORT')
        else:
            col.label(text="Select a node group to save", icon='INFO')
        
        layout.separator()
        
        # Search and controls
        row = layout.row(align=True)
        row.prop(scene, "nodelib_search", text="", icon='VIEWZOOM')
        row.operator("nodelib.refresh_library", text="", icon='FILE_REFRESH')
        
        # Sort options
        row = layout.row(align=True)
        row.prop(scene, "nodelib_sort", text="")
        
        layout.separator()
        
        # Library contents
        library = load_library()
        
        if not library["node_groups"]:
            box = layout.box()
            col = box.column(align=True)
            col.label(text="Library is empty", icon='INFO')
            col.label(text="Select a node group and")
            col.label(text="click 'Save' to start")
            return
        
        # Filter and sort
        current_type = context.space_data.tree_type
        filtered = [ng for ng in library["node_groups"] if ng["type"] == current_type]
        
        search = scene.nodelib_search.lower()
        if search:
            filtered = [ng for ng in filtered if 
                       search in ng["name"].lower() or 
                       any(search in tag.lower() for tag in ng.get("tags", []))]
        
        # Sort
        if scene.nodelib_sort == 'NAME':
            filtered.sort(key=lambda x: x["name"].lower())
        elif scene.nodelib_sort == 'DATE':
            filtered.sort(key=lambda x: x["versions"][-1]["timestamp"], reverse=True)
        elif scene.nodelib_sort == 'VERSIONS':
            filtered.sort(key=lambda x: len(x["versions"]), reverse=True)
        
        # Stats
        box = layout.box()
        row = box.row(align=True)
        row.label(text=f"{len(filtered)} Node Groups", icon='ASSET_MANAGER')
        
        if not filtered:
            layout.label(text="No results found", icon='INFO')
            return
        
        # Node groups
        for entry in filtered:
            box = layout.box()
            
            # Main header
            row = box.row(align=True)
            row.scale_y = 1.2
            
            # Collapsible arrow
            icon = 'TRIA_DOWN' if entry.get("expanded", False) else 'TRIA_RIGHT'
            op = row.operator("nodelib.toggle_expand", text="", icon=icon, emboss=False)
            op.node_name = entry["name"]
            
            # Add button (main action)
            op = row.operator("nodelib.add_node_from_library", text=entry["name"], icon='NODETREE')
            op.node_name = entry["name"]
            op.version = -1
            
            # Delete button
            op = row.operator("nodelib.delete_from_library", text="", icon='TRASH')
            op.node_name = entry["name"]
            
            # Tags row
            if entry.get("tags"):
                row = box.row()
                row.scale_y = 0.7
                row.label(text=" ".join([f"#{tag}" for tag in entry["tags"]]), icon='BOOKMARKS')
            
            # Version info row
            row = box.row()
            row.scale_y = 0.7
            latest_v = entry["versions"][-1]
            version_text = f"v{entry['latest_version']} • {len(entry['versions'])} versions"
            if latest_v.get('notes'):
                version_text += f" • {latest_v['notes'][:40]}"
            row.label(text=version_text, icon='DOCUMENTS')
            
            # Expanded version history
            if entry.get("expanded", False) and len(entry["versions"]) > 0:
                box.separator()
                col = box.column(align=True)
                
                for v in reversed(entry["versions"][-5:]):  # Show last 5
                    version_box = col.box()
                    version_row = version_box.row(align=True)
                    
                    # Version info
                    version_col = version_row.column(align=True)
                    version_col.scale_y = 0.8
                    version_col.label(text=f"Version {v['version']}", icon='DOT')
                    if v.get('notes'):
                        version_col.label(text=f"  {v['notes']}")
                    version_col.label(text=f"  {format_timestamp(v['timestamp'])}")
                    
                    # Actions
                    action_col = version_row.column(align=True)
                    op = action_col.operator("nodelib.add_node_from_library", text="", icon='IMPORT')
                    op.node_name = entry["name"]
                    op.version = v["version"]
                    
                    op = action_col.operator("nodelib.delete_version", text="", icon='X')
                    op.node_name = entry["name"]
                    op.version = v["version"]

class NODELIB_OT_ToggleExpand(bpy.types.Operator):
    bl_idname = "nodelib.toggle_expand"
    bl_label = ""
    bl_description = "Show/hide version history"
    bl_options = {'INTERNAL'}
    
    node_name: bpy.props.StringProperty()
    
    def execute(self, context):
        library = load_library()
        entry = next((ng for ng in library["node_groups"] if ng["name"] == self.node_name), None)
        
        if entry:
            entry["expanded"] = not entry.get("expanded", False)
            save_library(library)
            context.area.tag_redraw()
        
        return {'FINISHED'}

# Scene properties
def register_properties():
    bpy.types.Scene.nodelib_search = bpy.props.StringProperty(
        name="Search",
        description="Search node groups by name or tag"
    )
    
    bpy.types.Scene.nodelib_sort = bpy.props.EnumProperty(
        name="Sort By",
        items=[
            ('NAME', "Name", "Sort alphabetically"),
            ('DATE', "Date", "Sort by most recent"),
            ('VERSIONS', "Versions", "Sort by version count")
        ],
        default='NAME'
    )

def unregister_properties():
    del bpy.types.Scene.nodelib_search
    del bpy.types.Scene.nodelib_sort

# Registration
classes = (
    NODELIB_Preferences,
    NODELIB_OT_AddToLibrary,
    NODELIB_OT_AddNodeFromLibrary,
    NODELIB_OT_DeleteFromLibrary,
    NODELIB_OT_DeleteVersion,
    NODELIB_OT_RefreshLibrary,
    NODELIB_OT_OpenLibraryFolder,
    NODELIB_OT_ExportLibrary,
    NODELIB_OT_ImportLibrary,
    NODELIB_OT_ToggleExpand,
    NODELIB_PT_LibraryPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_properties()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    unregister_properties()

if __name__ == "__main__":
    register()