# Node Group Library Manager

**A professional version control and library management system for Blender node groups**

![Blender Version](https://img.shields.io/badge/Blender-3.0%2B-orange)
![Version](https://img.shields.io/badge/version-1.1.0-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-green)

Manage your shader, compositor, and geometry node groups like a pro with full version control, tagging, search, and import/export capabilities.

## ✨ Features

### 🎯 Core Functionality
- **Version Control**: Save multiple versions of node groups with detailed notes
- **One-Click Adding**: Click any library item to instantly add it to your editor
- **Smart Selection**: Recognizes currently selected node groups, not entire trees
- **Cross-Editor Support**: Works in Shader Editor, Compositor, and Geometry Nodes

### 🎨 Organization
- **Tags System**: Organize with custom tags (metal, procedural, PBR, etc.)
- **Search & Filter**: Instant search by name or tags
- **Smart Sorting**: Sort by name, date, or version count
- **Collapsible History**: Expand to see detailed version history

### 💾 Library Management
- **Custom Storage Path**: Choose where to store your library
- **Export/Import**: Share libraries as ZIP files or backup entire collections
- **Version Cleanup**: Delete specific versions or entire node groups
- **Open Library Folder**: Quick access to library files

### 🎯 User Experience
- **Clean UI**: Modern, intuitive interface in the N-panel
- **Visual Feedback**: Clear icons and status messages
- **Empty State Guidance**: Helpful instructions when starting out
- **Formatted Timestamps**: Human-readable dates and times

## 📦 Installation

### Method 1: Download Release
1. Download the latest `node_library_manager.zip` from [Releases](../../releases)
2. In Blender, go to `Edit` → `Preferences` → `Add-ons`
3. Click `Install...` and select the downloaded ZIP
4. Enable "Node Group Library Manager"

### Method 2: Manual Installation
1. Download `node_library_manager.py`
2. In Blender, go to `Edit` → `Preferences` → `Add-ons`
3. Click `Install...` and select the `.py` file
4. Enable "Node Group Library Manager"

## 🚀 Quick Start

### Saving Node Groups

1. **Create or select a node group** in Shader Editor, Compositor, or Geometry Nodes
2. **Select the group node** (not just being inside it)
3. Open the **N-panel** and find the "Node Library" tab
4. Click the **"Save"** button
5. Add version notes and tags (optional)
6. Done! Your node group is now in the library

### Using Node Groups

1. Open the **N-panel** in any node editor
2. Find your node group in the library
3. **Click the node group name** to add it to your editor
4. The node appears at your cursor location

### Version Management

- **View versions**: Click the arrow next to a node group to expand
- **Use specific version**: Click the import icon next to any version
- **Delete version**: Click the X icon next to a version
- **Delete node group**: Click the trash icon next to the node group name

## 📖 Usage Guide

### Tags
Add comma-separated tags when saving:
```
metal, procedural, PBR
```

Tags appear as `#metal #procedural #PBR` and are searchable.

### Search
Type in the search bar to filter by:
- Node group name
- Any tag

### Sorting
- **Name**: Alphabetical order
- **Date**: Most recently updated first
- **Versions**: Most versions first

### Custom Storage Path
1. Go to `Edit` → `Preferences` → `Add-ons`
2. Find "Node Group Library Manager"
3. Set your custom library path
4. Library automatically moves to new location

### Backup & Sharing
**Export Library:**
1. Go to addon preferences
2. Click "Export Library"
3. Save as ZIP file

**Import Library:**
1. Go to addon preferences
2. Click "Import Library"
3. Select ZIP file
4. Libraries merge automatically

## 🎯 Use Cases

### For Shader Artists
- Build a personal library of materials
- Version control complex shader setups
- Share shader libraries with team
- Tag by category (metal, fabric, stone)

### For Technical Artists
- Maintain utility node groups
- Track changes across projects
- Share standardized node setups
- Build studio-wide libraries

### For Educators
- Create teaching material libraries
- Share example node groups with students
- Version demonstrations and examples
- Organize by lesson or topic

## 🛠️ Technical Details

### Storage Location
**Default:** `[Blender Config]/scripts/addons/node_library_data/`

**Custom:** Set in addon preferences

### File Structure
```
node_library_data/
├── library.json          # Library metadata
└── node_groups/          # Versioned .blend files
    ├── MyShader_v1.blend
    ├── MyShader_v2.blend
    └── ...
```

### Compatibility
- **Blender Version:** 3.0 and above
- **Node Types:** Shader, Compositor, Geometry
- **Operating Systems:** Windows, macOS, Linux

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
git clone https://github.com/yourusername/node-library-manager.git
cd node-library-manager
# Symlink to Blender addons folder for development
```

## 📝 Changelog

### v1.1.0 (Current)
- Complete UI redesign with modern layout
- Added tags system for organization
- Search and sort functionality
- Custom storage path support
- Export/Import library as ZIP
- Collapsible version history
- Formatted timestamps
- Better error handling and feedback

### v1.0.0
- Initial release
- Basic version control
- Save and restore node groups
- Delete versions and node groups

## 📄 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Clay MacDonald**

## 🙏 Acknowledgments

- Blender Foundation for the amazing software
- Blender community for inspiration and feedback
- Contributors and users for making this better

## 📮 Support

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Documentation**: [Wiki](../../wiki) (coming soon)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ for the Blender community**