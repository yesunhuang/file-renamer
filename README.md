# File Renamer

A simple yet powerful utility for batch renaming files with customizable patterns.

## Features

- Rename multiple files at once with customizable patterns
- Preview changes before applying
- Option to remove existing prefixes and order numbers
- Support for numbered sequences with custom formatting
- Cross-platform compatibility

## Installation

### Option 1: Download the executable (Windows)
Download the latest executable from the [Releases](https://github.com/yourusername/file-renamer/releases) page.

### Option 2: Run from source
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/file-renamer.git
   ```
2. Navigate to the project directory:
   ```
   cd file-renamer
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```
Follow the prompts in the user interface to rename files or folders as desired.

## Configuration
Default settings can be modified in the `config/default_config.json` file. This includes default prefixes and ordering formats.

## Testing
To run the tests, navigate to the `tests` directory and execute:
```
pytest
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.