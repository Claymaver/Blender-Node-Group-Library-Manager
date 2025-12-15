# Node Group Library Manager

**A professional version control and library management system for Blender node groups**

![Blender Version](https://img.shields.io/badge/Blender-3.0%2B-orange)
![Version](https://img.shields.io/badge/version-1.1.0-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-green)

Manage your shader, compositor, and geometry node groups like a pro with full version control, tagging, search, and import/export capabilities.

## 📥 Installation

1. Download `node_library_manager.py`
2. Open Blender → **Edit** → **Preferences** → **Add-ons**
3. Click **Install** and select the file
4. Enable **Node Group Library Manager**
5. Open Shader Editor or Compositor and press **N** to see the panel

---

## ✨ Features

### Version Control
- Save multiple versions of each node group
- Add version notes to track changes
- Restore any previous version instantly
- View version history with timestamps

![version info](images/Screenshot_5.png)

### Smart Organization
- Tag your node groups for easy discovery
- Search by name or tag
- Sort by name, date, or version count
- Collapsible version history

![Tags](images/Screenshot_4.png)

### Easy Workflow
- Click any node group to add it to your editor
- Works in Shader Editor, Compositor, and Geometry Nodes
- One-click save from selected node groups
- Clean, intuitive interface

![version info](images/Screenshot_3.png)

### Backup & Sharing
- Export entire library as ZIP
- Import libraries from other users
- Set custom storage location
- Open library folder directly

![Tags](images/Screenshot_6.png)

---

## 🚀 Quick Start

### Saving a Node Group

1. **Create or select** a node group in your editor
2. **Click the node group node** to select it
3. **Click "Save"** in the Node Library panel
4. **Add version notes and tags** (optional)
5. Done! Your node group is now in the library

### Using a Saved Node Group

1. **Open** Shader Editor or Compositor
2. **Find your node group** in the library panel
3. **Click the node group name** to add it to your editor
4. The node appears at your cursor location

### Version History

Click the **arrow** next to any node group to see all versions:
- View version notes and dates
- Import specific versions
- Delete old versions

---

## 📖 Usage Guide

### The Panel

**Top Section:**
- Shows currently selected node group
- "Save" button to add to library

**Search & Sort:**
- Search bar filters by name and tags
- Sort dropdown (Name, Date, Versions)

**Library:**
- All your saved node groups
- Click to add to editor
- Expand arrow shows version history
- Trash icon deletes entire node group

### Tags

Add tags when saving to organize your library:
```
metal, procedural, PBR
```

Tags appear with # symbols and are searchable.

### Preferences

Access in **Edit** → **Preferences** → **Add-ons** → **Node Group Library Manager**

**Options:**
- **Library Path:** Set custom storage location
- **Open Library Folder:** Browse your files
- **Export Library:** Create backup ZIP
- **Import Library:** Merge another library

---

## 💡 Tips

- **Use version notes** to track what changed in each version
- **Tag consistently** for easier searching (e.g., always use "metal" not "metals")
- **Export regularly** to backup your library
- **Share libraries** with your team via ZIP export/import
- **Keep the latest version** clean and well-tested

---

## 🐛 Troubleshooting

**"No node group selected"**
- Make sure you've clicked on a node group node, not just any node

**Node group doesn't appear after clicking**
- Check your cursor is inside the editor area
- Make sure you're in the correct editor type (Shader/Compositor/Geometry)

**Can't find saved node groups**
- Check the sort/search isn't filtering them out
- Refresh the library with the refresh button
- Verify the correct editor type (shader groups only show in shader editor)

---

## 📝 Version History

### v1.1.0 (Current)
- Added custom storage path
- Added search and sort functionality
- Added tag system
- Added collapsible version history
- Added export/import library
- Improved UI design
- Better version management

### v1.0.0
- Initial release
- Basic save/load functionality
- Version control
- Multi-editor support

---

## 🤝 Contributing

Found a bug or have a feature request? Feel free to reach out or submit an issue.

---

## 📄 License

This addon is provided as-is for use in Blender projects.

---

**Made with ❤️ for the Blender community**
