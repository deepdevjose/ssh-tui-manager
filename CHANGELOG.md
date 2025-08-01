# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [2.1.1] - 2025-08-01

### Enhanced
- **Robust Error Handling**: Comprehensive error handling for configuration files
- **Automatic Backup**: Corrupted JSON files are automatically backed up before fallback
- **Data Validation**: Full validation of configuration data structure and types
- **UTF-8 Support**: International character support with proper encoding
- **Permission Handling**: Graceful handling of file permission errors
- **Save Operations**: Robust save_config() with status feedback and error recovery

### Added
- Configuration loading with multiple fallback strategies
- Automatic migration of legacy field names (usuarios → users)
- Required field validation with sensible defaults (IP, users, color)
- Clear error messages with professional colored output
- Module import safety with `__name__ == "__main__"` guard
- Data integrity preservation during save failures

### Improved
- User feedback for all save operation failures
- Professional error messaging and user guidance
- Enterprise-ready stability for production environments
- Maintains functionality even under adverse conditions
- Comprehensive testing against multiple failure scenarios

---

## [2.1.0] - 2025-08-01

### Added
- **Arrow Key Navigation**: Full keyboard navigation with ↑↓ arrows for menu selection
- **Professional Terminal Theme**: 256-color ANSI styling with blue professional color scheme
- **Cancellation Support**: Comprehensive cancellation with keywords 'cancel', 'exit', 'quit'
- **Quick Connect Feature**: Direct connection for VMs with single users
- **Input Validation**: Robust validation for VM names, IP addresses, and usernames
- **Visual Controls Guide**: Clear keyboard controls displayed in all menus

### Enhanced
- **User Experience**: Intuitive navigation with highlighted selections and visual feedback
- **Terminal Interface**: Professional appearance with borders, highlights, and consistent styling
- **Error Handling**: Improved validation loops with clear error messages
- **Cancellation Flow**: Ability to cancel operations at any point during VM/user creation
- **Quick Actions**: Streamlined workflow for common operations

### Added Features
- Arrow key menu navigation with visual selection highlighting
- Direct number key selection (0-9) for quick menu access
- Professional blue color theme with consistent styling throughout
- Comprehensive input validation for all user inputs
- Visual feedback for successful operations and errors
- Cancellation options at every input step in multi-step processes

### Technical
- Enhanced `arrow_menu()` function with full keyboard support
- Professional ANSI color codes (RED: 196, GREEN: 46, CYAN: 51, BLUE: 39)
- Windows-specific keyboard input handling with msvcrt
- Improved user interface consistency across all menus
- Enhanced error messaging with colored output

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
