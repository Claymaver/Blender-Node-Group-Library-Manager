# Contributing to Node Group Library Manager

First off, thank you for considering contributing! 🎉

The following is a set of guidelines for contributing to the Node Group Library Manager. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by respect, kindness, and constructive collaboration. By participating, you are expected to uphold these values.

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** and what you expected
- **Include Blender version** and operating system
- **Include screenshots** if applicable

**Example bug report:**

```markdown
**Bug**: Cannot import node groups with long names

**Steps to reproduce:**
1. Create a node group with name longer than 50 characters
2. Save to library
3. Try to import from library

**Expected**: Node group imports successfully
**Actual**: Error message appears

**Environment:**
- Blender 4.0.2
- Windows 11
- Addon v1.1.0
```

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description** of the suggested enhancement
- **Provide specific examples** to demonstrate the steps
- **Describe the current behavior** and explain the behavior you expected
- **Explain why this enhancement would be useful**

### 📝 Code Contributions

#### Good First Issues

Look for issues labeled `good first issue` - these are great for newcomers!

#### Feature Development

1. **Check existing issues/PRs** to avoid duplicate work
2. **Open an issue first** to discuss major changes
3. **Fork the repository** and create your branch
4. **Write clean code** following our standards
5. **Test thoroughly** in multiple Blender versions
6. **Submit a pull request**

## Development Setup

### Prerequisites

- Blender 3.0 or newer
- Git
- Python 3.10+ (matches Blender's Python)
- Text editor or IDE (VS Code recommended)

### Setting Up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/node-library-manager.git
   cd node-library-manager
   ```

2. **Create a symlink to Blender's addons folder:**
   
   **Windows:**
   ```powershell
   mklink /D "%APPDATA%\Blender Foundation\Blender\3.6\scripts\addons\node_library_manager" "C:\path\to\node-library-manager"
   ```
   
   **macOS/Linux:**
   ```bash
   ln -s /path/to/node-library-manager ~/.config/blender/3.6/scripts/addons/node_library_manager
   ```

3. **Enable developer mode in Blender:**
   - Edit → Preferences → Interface
   - Enable "Developer Extras"
   - Enable "Python Tooltips"

4. **Reload addon after changes:**
   - F3 → "Reload Scripts"
   - Or restart Blender

### Project Structure

```
node_library_manager.py    # Main addon file
├── bl_info               # Addon metadata
├── Preferences           # Addon preferences
├── Operators             # All operations
├── Panels                # UI panels
└── Utility functions     # Helper functions
```

## Coding Standards

### Python Style

Follow [PEP 8](https://pep8.org/) with these specifics:

- **Indentation**: 4 spaces (no tabs)
- **Line length**: 100 characters max
- **Naming**:
  - Classes: `PascalCase` (e.g., `NODELIB_OT_AddToLibrary`)
  - Functions: `snake_case` (e.g., `get_library_path`)
  - Constants: `UPPER_SNAKE_CASE`
  - Properties: `snake_case`

### Blender Conventions

- **Operator IDs**: `nodelib.operation_name`
- **Class naming**: `NODELIB_OT_OperationName` (Operator), `NODELIB_PT_PanelName` (Panel)
- **bl_idname**: Must match operator ID
- **bl_label**: User-friendly name
- **bl_description**: Tooltip text

### Code Example

```python
class NODELIB_OT_ExampleOperation(bpy.types.Operator):
    """Example operator with proper structure"""
    bl_idname = "nodelib.example_operation"
    bl_label = "Example Operation"
    bl_description = "This is what appears in the tooltip"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    my_property: bpy.props.StringProperty(
        name="My Property",
        description="Description for the property",
        default=""
    )
    
    def execute(self, context):
        # Your code here
        self.report({'INFO'}, "Operation completed")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
```

### Comments

- Write **why**, not **what**
- Use docstrings for functions and classes
- Keep inline comments concise

```python
def get_selected_node_group(context):
    """
    Get the node group from the currently selected node.
    
    Returns None if no valid node group is selected.
    """
    # Check if we're in a node editor
    space = context.space_data
    if not space or space.type != 'NODE_EDITOR':
        return None
    
    # ... rest of function
```

## Commit Messages

### Format

```
type(scope): brief description

Detailed explanation of changes (optional)

- Additional bullet points (optional)
- More details

Closes #123
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples

```
feat(library): add thumbnail preview support

Added support for generating and displaying thumbnails
for shader node groups. Thumbnails are cached in the
library folder.

Closes #45
```

```
fix(ui): correct version sorting order

Fixed issue where versions were sorted alphabetically
instead of numerically.

Fixes #67
```

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tested in Blender 3.0+ and 4.0+
- [ ] No console errors or warnings
- [ ] Documentation updated (README, CHANGELOG)
- [ ] Commit messages follow guidelines
- [ ] Branch is up to date with main

### Submitting

1. **Push to your fork:**
   ```bash
   git push origin feature/amazing-feature
   ```

2. **Open a Pull Request** on GitHub

3. **Fill in the PR template:**
   - Description of changes
   - Related issue numbers
   - Testing performed
   - Screenshots (if UI changes)

### PR Template

```markdown
## Description
Brief description of what this PR does

## Related Issues
Closes #123

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tested in Blender 3.6
- [ ] Tested in Blender 4.0
- [ ] Tested on Windows
- [ ] Tested on macOS
- [ ] Tested on Linux

## Screenshots
(if applicable)

## Additional Notes
Any additional information
```

### Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, it will be merged
- Your contribution will be credited in CHANGELOG

## Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes (e.g., 2.0.0)
- **MINOR**: New features, backwards compatible (e.g., 1.2.0)
- **PATCH**: Bug fixes, backwards compatible (e.g., 1.1.1)

### Creating a Release

Maintainers only:

1. Update version in `node_library_manager.py`
2. Update `CHANGELOG.md`
3. Commit changes
4. Create and push tag: `git tag v1.2.0 && git push origin v1.2.0`
5. GitHub Actions automatically creates release

## Questions?

- Open an issue with the `question` label
- Start a discussion in GitHub Discussions
- Contact maintainers

## Recognition

Contributors will be:
- Listed in CHANGELOG for their contributions
- Credited in release notes
- Added to README acknowledgments

Thank you for contributing! 🚀