# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [2.0.1] - 2025-08-01

### Added
- Inline user management in VM connection menu (add/remove users directly)
- Enhanced default VM configurations (Debian VM and Rocky VM with proper IPs)
- Confirmation messages for all CRUD operations (add/edit/delete VMs and users)
- "Press Enter to return" prompts for better navigation flow

### Changed
- Streamlined admin menu workflow with clearer edit options
- Simplified VM editing to focus on IP address changes only
- Improved menu labels: "Connect as [user]" instead of just username
- Enhanced user experience with better feedback messages

### Improved
- Navigation flow between menus is more intuitive
- User management moved from admin panel to individual VM menus
- More responsive and user-friendly interface

---

## [2.0.0] - 2025-08-01

### Added
- JSON configuration persistence (`vms.json`) for VM and user data
- Complete admin menu for VM management (add/edit/delete VMs)
- ANSI color support for enhanced visual interface
- Robust configuration handling with backward compatibility
- Defensive programming for missing JSON fields
- Color-coded VM display in main menu
- Automatic migration from Spanish "usuarios" to English "users"

### Changed
- Complete code refactor from Spanish to English American
- SSH connections now open in separate CMD windows instead of same terminal
- Enhanced error handling and input validation
- Configuration format supports both old and new JSON structures

### Fixed
- KeyError crashes when VM configuration missing color or users fields
- JSON compatibility issues between different configuration versions
- Encoding and character display issues in terminal

### Technical
- Improved load_config() with fallback mechanisms
- Added save_config() for automatic persistence
- Implemented COLORS mapping for consistent styling
- Enhanced clear_screen() function for cross-platform compatibility

---

## [1.0.0] - 2025-08-01

### Added
- Initial interactive SSH menu using standard Python.
- Option to select a virtual machine (VM).
- Option to select a user per VM.
- SSH connection opens in the same terminal.
- Basic input validation for user and VM selection.

### Notes
- This is the first working version of the project.
- No external libraries are required.
