# File Renamer v1.3.0

A powerful utility for batch renaming files and managing folder structures, now with advanced AI capabilities.

## Features

- **File Renaming**
  - Rename multiple files at once with customizable prefix formats
  - Support for sequential numbering and ordering
  - Preview changes before applying
  - Option to remove existing prefixes and order numbers
  - **Include Folders**: Rename directories alongside files

- **Folder Management**
  - **Collapse Redundant Folders**: Identify and merge nested folder structures (e.g., `parent/child` -> `parent_child`)
  - **Uncollapse Folders**: Expand folders with underscore-separated names into nested structures
  - Recursive processing support

- **AI Renaming**
  - **Multi-Provider Support**: Choose between Google Gemini and OpenAI models
  - **Model Selection**: Select specific models (e.g., Gemini 1.5 Flash, GPT-4)
  - **Prompt Preview**: View the exact system instruction and file list sent to the AI
  - **Smart Suggestions**: Generate meaningful names based on file content or patterns

- **User Experience**
  - Intuitive menu-driven interface
  - Modern GUI with dedicated tabs for Manual, AI, and Folder operations
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
1. Select "Rename files/folders" from the main menu or "Manual Rename" tab in GUI
2. Enter the directory path containing files to rename
3. Specify a prefix format (e.g., "photo_", "doc_v2_")
4. Choose whether to enable ordering (sequential numbering)
5. Choose whether to remove existing prefixes
6. Review the preview and confirm to apply changes

### Folder Management
1. **Collapsing Folders**: Select "Collapse redundant folders" to identify and merge nested folder structures
2. **Uncollapsing Folders**: Select "Uncollapse folders by underscore" to expand folders with underscore-separated names into nested structures

### AI Renaming
1. Go to the "AI Rename" tab
2. Select your provider (Gemini/OpenAI) and Model
3. Enter a natural language instruction (e.g., "Rename these music files to Artist - Title format")
4. Click "Preview Prompt" to verify what will be sent
5. Click "Generate Suggestions" to see AI-proposed names
6. Apply the changes if satisfied

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.