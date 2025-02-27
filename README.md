# File Renamer v1.2.0

A powerful utility for batch renaming files and managing folder structures.

## Features

- **File Renaming**
  - Rename multiple files at once with customizable prefix formats
  - Support for sequential numbering and ordering
  - Preview changes before applying
  - Option to remove existing prefixes and order numbers

- **Folder Management**
  - Rename folders along with files
  - Collapse redundant folder structures
  - Uncollapse folders using underscore separators

- **User Experience**
  - Intuitive menu-driven interface
  - Error handling and warnings
  - Cross-platform compatibility

## Installation

### Option 1: Download the executable (Windows)
Download the latest executable from the [Releases](https://github.com/yesunhuang/file-renamer/releases) page.

### Option 2: Run from source
1. Clone the repository:
   ```
   git clone https://github.com/yesunhuang/file-renamer.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python run.py
   ```

## Usage

### File Renaming
1. Select "Rename files/folders" from the main menu
2. Enter the directory path containing files to rename
3. Specify a prefix format (e.g., "photo_", "doc_v2_")
4. Choose whether to enable ordering (sequential numbering)
5. Choose whether to remove existing prefixes
6. Review the preview and confirm to apply changes

### Folder Management
1. **Collapsing Folders**: Select "Collapse redundant folders" to identify and merge nested folder structures
2. **Uncollapsing Folders**: Select "Uncollapse folders by underscore" to expand folders with underscore-separated names into nested structures

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.