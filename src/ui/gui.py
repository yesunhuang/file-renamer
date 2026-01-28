import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget, 
                             QFileDialog, QComboBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QCheckBox, QGroupBox, QDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from src.config_manager import ConfigManager
from src.ai_renamer import AIRenamer
from src.file_operations import rename_files
from src.rename_utils import generate_new_name, apply_regex_rename
from src.folder_operations import collapse_redundant_folders, uncollapse_folders, identify_redundant_folders

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    return os.path.join(base_path, relative_path)

class ModelFetcherThread(QThread):
    models_fetched = pyqtSignal(str, list)

    def __init__(self, ai_renamer, provider):
        super().__init__()
        self.ai_renamer = ai_renamer
        self.provider = provider

    def run(self):
        models = self.ai_renamer.get_available_models(self.provider)
        self.models_fetched.emit(self.provider, models)

class PromptPreviewDialog(QDialog):
    def __init__(self, system_prompt, full_prompt, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI Prompt Preview")
        self.setGeometry(200, 200, 600, 500)
        self.setWindowIcon(QIcon(resource_path("file_renamer_icon.ico")))
        
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("<b>System Instruction:</b>"))
        sys_text = QTextEdit()
        sys_text.setPlainText(system_prompt)
        sys_text.setReadOnly(True)
        sys_text.setMaximumHeight(100)
        layout.addWidget(sys_text)
        
        layout.addWidget(QLabel("<b>Full Prompt (User Message):</b>"))
        full_text = QTextEdit()
        full_text.setPlainText(full_prompt)
        full_text.setReadOnly(True)
        layout.addWidget(full_text)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

class FileRenamerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.ai_renamer = AIRenamer(self.config_manager)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Advanced AI File Renamer")
        self.setGeometry(100, 100, 900, 700)
        self.setWindowIcon(QIcon(resource_path("file_renamer_icon.ico")))
        
        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_manual_tab()
        self.create_ai_tab()
        self.create_folder_tools_tab()
        self.create_settings_tab()
        
        # Apply styling
        self.apply_styles()

    def apply_styles(self):
        # Simple modern styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #007bff;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit, QTextEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)

    def create_manual_tab(self):
        self.manual_tab = QWidget()
        layout = QVBoxLayout(self.manual_tab)
        
        # Directory Selection
        dir_layout = QHBoxLayout()
        self.manual_dir_input = QLineEdit()
        self.manual_dir_input.setPlaceholderText("Select Directory...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_directory(self.manual_dir_input))
        dir_layout.addWidget(self.manual_dir_input)
        dir_layout.addWidget(browse_btn)
        layout.addLayout(dir_layout)
        
        # Options
        options_group = QGroupBox("Renaming Options")
        options_layout = QVBoxLayout()
        
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("Prefix Format (e.g., 'Image_')")
        options_layout.addWidget(QLabel("Prefix:"))
        options_layout.addWidget(self.prefix_input)
        
        self.ordering_check = QCheckBox("Enable Ordering")
        options_layout.addWidget(self.ordering_check)
        
        self.remove_prefix_check = QCheckBox("Remove Existing Prefixes")
        options_layout.addWidget(self.remove_prefix_check)

        # Regex Section
        regex_group = QGroupBox("Regex Renaming (Advanced)")
        regex_layout = QVBoxLayout()
        
        self.regex_enable_check = QCheckBox("Enable Regex")
        self.regex_enable_check.stateChanged.connect(self.toggle_regex_inputs)
        regex_layout.addWidget(self.regex_enable_check)
        
        regex_form = QHBoxLayout()
        self.regex_pattern_input = QLineEdit()
        self.regex_pattern_input.setPlaceholderText("Pattern (e.g., ^(\\w+)_(\\d+))")
        self.regex_pattern_input.setEnabled(False)
        
        self.regex_repl_input = QLineEdit()
        self.regex_repl_input.setPlaceholderText("Replacement (e.g., \\2 - \\1)")
        self.regex_repl_input.setEnabled(False)
        
        regex_form.addWidget(QLabel("Pattern:"))
        regex_form.addWidget(self.regex_pattern_input)
        regex_form.addWidget(QLabel("Replace:"))
        regex_form.addWidget(self.regex_repl_input)
        
        regex_layout.addLayout(regex_form)
        regex_group.setLayout(regex_layout)
        options_layout.addWidget(regex_group)

        self.manual_include_folders = QCheckBox("Include Folders")
        options_layout.addWidget(self.manual_include_folders)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        preview_btn = QPushButton("Preview Changes")
        preview_btn.clicked.connect(self.preview_manual_rename)
        apply_btn = QPushButton("Apply Rename")
        apply_btn.clicked.connect(self.apply_manual_rename)
        btn_layout.addWidget(preview_btn)
        btn_layout.addWidget(apply_btn)
        layout.addLayout(btn_layout)
        
        # Results Table
        self.manual_table = QTableWidget()
        self.manual_table.setColumnCount(2)
        self.manual_table.setHorizontalHeaderLabels(["Original Name", "New Name"])
        self.manual_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.manual_table)
        
        self.tabs.addTab(self.manual_tab, "Manual Rename")

    def create_ai_tab(self):
        self.ai_tab = QWidget()
        layout = QVBoxLayout(self.ai_tab)
        
        # Directory Selection
        dir_layout = QHBoxLayout()
        self.ai_dir_input = QLineEdit()
        self.ai_dir_input.setPlaceholderText("Select Directory...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_directory(self.ai_dir_input))
        dir_layout.addWidget(self.ai_dir_input)
        dir_layout.addWidget(browse_btn)
        layout.addLayout(dir_layout)
        
        # AI Configuration
        ai_group = QGroupBox("AI Configuration")
        ai_layout = QVBoxLayout()
        
        # Provider Selection
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["gemini", "openai"])
        # Set default from config
        last_provider = self.config_manager.load_config().get("last_provider", "gemini")
        index = self.provider_combo.findText(last_provider)
        if index >= 0:
            self.provider_combo.setCurrentIndex(index)
        provider_layout.addWidget(self.provider_combo)
        provider_layout.addWidget(self.provider_combo)
        
        # Model Selection
        provider_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.provider_combo.currentTextChanged.connect(self.update_model_list)
        self.model_combo.currentTextChanged.connect(self.save_model_preference)
        provider_layout.addWidget(self.model_combo)
        
        ai_layout.addLayout(provider_layout)
        
        # Initialize models
        self.update_model_list(self.provider_combo.currentText())
        
        # Prompt Input
        ai_layout.addWidget(QLabel("Renaming Instruction:"))
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("E.g., 'Rename these files to be more descriptive based on their current names. Use snake_case.'")
        self.prompt_input.setMaximumHeight(100)
        ai_layout.addWidget(self.prompt_input)
        
        ai_group.setLayout(ai_layout)
        ai_group.setLayout(ai_layout)
        layout.addWidget(ai_group)

        # Options
        options_layout = QHBoxLayout()
        self.ai_include_folders = QCheckBox("Include Folders")
        options_layout.addWidget(self.ai_include_folders)
        layout.addLayout(options_layout)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        preview_prompt_btn = QPushButton("Preview Prompt")
        preview_prompt_btn.clicked.connect(self.preview_ai_prompt)
        generate_btn = QPushButton("Generate Suggestions")
        generate_btn.clicked.connect(self.generate_ai_suggestions)
        apply_btn = QPushButton("Apply Rename")
        apply_btn.clicked.connect(self.apply_ai_rename)
        btn_layout.addWidget(preview_prompt_btn)
        btn_layout.addWidget(generate_btn)
        btn_layout.addWidget(apply_btn)
        layout.addLayout(btn_layout)
        
        # Results Table
        self.ai_table = QTableWidget()
        self.ai_table.setColumnCount(2)
        self.ai_table.setHorizontalHeaderLabels(["Original Name", "New Name"])
        self.ai_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.ai_table)
        
        self.tabs.addTab(self.ai_tab, "AI Rename")

    def create_folder_tools_tab(self):
        self.folder_tab = QWidget()
        layout = QVBoxLayout(self.folder_tab)
        
        # --- Collapse Section ---
        collapse_group = QGroupBox("Collapse Redundant Folders")
        collapse_layout = QVBoxLayout()
        
        # Directory
        c_dir_layout = QHBoxLayout()
        self.collapse_dir_input = QLineEdit()
        self.collapse_dir_input.setPlaceholderText("Select Directory to Collapse...")
        c_browse_btn = QPushButton("Browse")
        c_browse_btn.clicked.connect(lambda: self.browse_directory(self.collapse_dir_input))
        c_dir_layout.addWidget(self.collapse_dir_input)
        c_dir_layout.addWidget(c_browse_btn)
        collapse_layout.addLayout(c_dir_layout)
        
        # Options
        self.recursive_check = QCheckBox("Recursive Collapse")
        self.recursive_check.setChecked(True)
        collapse_layout.addWidget(self.recursive_check)
        
        # Buttons
        c_btn_layout = QHBoxLayout()
        c_preview_btn = QPushButton("Preview Collapse")
        c_preview_btn.clicked.connect(self.preview_collapse)
        c_apply_btn = QPushButton("Collapse Folders")
        c_apply_btn.clicked.connect(self.apply_collapse)
        c_btn_layout.addWidget(c_preview_btn)
        c_btn_layout.addWidget(c_apply_btn)
        collapse_layout.addLayout(c_btn_layout)
        
        collapse_group.setLayout(collapse_layout)
        layout.addWidget(collapse_group)
        
        # --- Uncollapse Section ---
        uncollapse_group = QGroupBox("Uncollapse Folders")
        uncollapse_layout = QVBoxLayout()
        
        # Directory
        u_dir_layout = QHBoxLayout()
        self.uncollapse_dir_input = QLineEdit()
        self.uncollapse_dir_input.setPlaceholderText("Select Directory to Uncollapse...")
        u_browse_btn = QPushButton("Browse")
        u_browse_btn.clicked.connect(lambda: self.browse_directory(self.uncollapse_dir_input))
        u_dir_layout.addWidget(self.uncollapse_dir_input)
        u_dir_layout.addWidget(u_browse_btn)
        uncollapse_layout.addLayout(u_dir_layout)
        
        # Options
        u_opts_layout = QHBoxLayout()
        u_opts_layout.addWidget(QLabel("Min Parts:"))
        self.min_parts_input = QLineEdit("2")
        self.min_parts_input.setFixedWidth(50)
        u_opts_layout.addWidget(self.min_parts_input)
        u_opts_layout.addStretch()
        uncollapse_layout.addLayout(u_opts_layout)
        
        # Buttons
        u_btn_layout = QHBoxLayout()
        u_preview_btn = QPushButton("Preview Uncollapse")
        u_preview_btn.clicked.connect(self.preview_uncollapse)
        u_apply_btn = QPushButton("Uncollapse Folders")
        u_apply_btn.clicked.connect(self.apply_uncollapse)
        u_btn_layout.addWidget(u_preview_btn)
        u_btn_layout.addWidget(u_apply_btn)
        uncollapse_layout.addLayout(u_btn_layout)
        
        uncollapse_group.setLayout(uncollapse_layout)
        layout.addWidget(uncollapse_group)
        
        # Results Area
        self.folder_results = QTextEdit()
        self.folder_results.setReadOnly(True)
        layout.addWidget(QLabel("Results/Preview:"))
        layout.addWidget(self.folder_results)
        
        self.tabs.addTab(self.folder_tab, "Folder Tools")

    def create_settings_tab(self):
        self.settings_tab = QWidget()
        layout = QVBoxLayout(self.settings_tab)
        
        form_layout = QVBoxLayout()
        
        # Gemini Key
        form_layout.addWidget(QLabel("Gemini API Key:"))
        self.gemini_key_input = QLineEdit()
        self.gemini_key_input.setEchoMode(QLineEdit.Password)
        self.gemini_key_input.setText(self.config_manager.get_api_key("gemini"))
        form_layout.addWidget(self.gemini_key_input)
        
        # OpenAI Key
        form_layout.addWidget(QLabel("OpenAI API Key:"))
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.Password)
        self.openai_key_input.setText(self.config_manager.get_api_key("openai"))
        form_layout.addWidget(self.openai_key_input)
        
        layout.addLayout(form_layout)
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
        self.tabs.addTab(self.settings_tab, "Settings")

    def browse_directory(self, input_field):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            input_field.setText(directory)

    def save_settings(self):
        gemini_key = self.gemini_key_input.text().strip()
        openai_key = self.openai_key_input.text().strip()
        
        self.config_manager.set_api_key("gemini", gemini_key)
        self.config_manager.set_api_key("openai", openai_key)
        
        QMessageBox.information(self, "Success", "Settings saved successfully!")

    def update_model_list(self, provider):
        self.model_combo.clear()
        self.model_combo.addItem("Loading...")
        self.model_combo.setEnabled(False)
        
        self.fetcher_thread = ModelFetcherThread(self.ai_renamer, provider)
        self.fetcher_thread.models_fetched.connect(self.on_models_fetched)
        self.fetcher_thread.start()

    def on_models_fetched(self, provider, models):
        # Verify if the current provider is still the same (user might have switched quickly)
        if self.provider_combo.currentText() != provider:
            return
            
        self.model_combo.clear()
        self.model_combo.addItems(models)
        self.model_combo.setEnabled(True)
        
        # Set selected model from config
        saved_model = self.config_manager.get_model(provider)
        if saved_model and saved_model in models:
            self.model_combo.setCurrentText(saved_model)

    def save_model_preference(self, model):
        if not model: return
        provider = self.provider_combo.currentText()
        self.config_manager.set_model(provider, model)

    def get_items_in_dir(self, directory, include_folders=False):
        if not directory or not os.path.exists(directory):
            return []
        items = []
        for f in os.listdir(directory):
            full_path = os.path.join(directory, f)
            if os.path.isfile(full_path) or (include_folders and os.path.isdir(full_path)):
                items.append(full_path)
        return items

    def preview_manual_rename(self):
        directory = self.manual_dir_input.text()
        include_folders = self.manual_include_folders.isChecked()
        files = self.get_items_in_dir(directory, include_folders)
        if not files:
            QMessageBox.warning(self, "Warning", "No files found or invalid directory.")
            return

        prefix = self.prefix_input.text()
        ordering = self.ordering_check.isChecked()
        
        # Regex params
        use_regex = self.regex_enable_check.isChecked()
        regex_pattern = self.regex_pattern_input.text()
        regex_repl = self.regex_repl_input.text()
        
        # Simple preview logic (simplified version of main.py logic)
        self.manual_table.setRowCount(len(files))
        self.manual_preview_data = [] # Store for applying
        
        for i, file_path in enumerate(files):
            old_name = os.path.basename(file_path)
            
            # Apply Regex First if enabled
            intermediate_name = old_name
            if use_regex:
                intermediate_name = apply_regex_rename(old_name, regex_pattern, regex_repl)
                
            order_val = i + 1 if ordering else None
            new_name = generate_new_name(intermediate_name, prefix, order_val)
            
            self.manual_table.setItem(i, 0, QTableWidgetItem(old_name))
            self.manual_table.setItem(i, 1, QTableWidgetItem(new_name))
            self.manual_preview_data.append((file_path, new_name))

    def apply_manual_rename(self):
        if not hasattr(self, 'manual_preview_data') or not self.manual_preview_data:
            QMessageBox.warning(self, "Warning", "Please preview changes first.")
            return
            
        try:
            count = 0
            for old_path, new_name in self.manual_preview_data:
                dir_path = os.path.dirname(old_path)
                new_path = os.path.join(dir_path, new_name)
                if old_path != new_path:
                    os.rename(old_path, new_path)
                    count += 1
            
            QMessageBox.information(self, "Success", f"Renamed {count} files.")
            self.manual_preview_data = []
            self.manual_table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def generate_ai_suggestions(self):
        directory = self.ai_dir_input.text()
        include_folders = self.ai_include_folders.isChecked()
        files = self.get_items_in_dir(directory, include_folders)
        if not files:
            QMessageBox.warning(self, "Warning", "No files found or invalid directory.")
            return
            
        prompt = self.prompt_input.toPlainText()
        if not prompt:
            QMessageBox.warning(self, "Warning", "Please enter a renaming instruction.")
            return
            
        provider = self.provider_combo.currentText()
        model = self.model_combo.currentText()
        
        try:
            suggestions = self.ai_renamer.get_rename_suggestions(files, prompt, provider, model)
            
            self.ai_table.setRowCount(len(suggestions))
            self.ai_preview_data = suggestions # Store for applying
            
            for i, (old_path, new_name) in enumerate(suggestions):
                old_name = os.path.basename(old_path)
                self.ai_table.setItem(i, 0, QTableWidgetItem(old_name))
                self.ai_table.setItem(i, 1, QTableWidgetItem(new_name))
                
        except Exception as e:
            QMessageBox.critical(self, "AI Error", str(e))

    def apply_ai_rename(self):
        if not hasattr(self, 'ai_preview_data') or not self.ai_preview_data:
            QMessageBox.warning(self, "Warning", "Please generate suggestions first.")
            return
            
        try:
            count = 0
            for old_path, new_name in self.ai_preview_data:
                dir_path = os.path.dirname(old_path)
                new_path = os.path.join(dir_path, new_name)
                if old_path != new_path:
                    os.rename(old_path, new_path)
                    count += 1
            
            QMessageBox.information(self, "Success", f"Renamed {count} files.")
            self.ai_preview_data = []
            self.ai_table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def preview_ai_prompt(self):
        directory = self.ai_dir_input.text()
        include_folders = self.ai_include_folders.isChecked()
        files = self.get_items_in_dir(directory, include_folders)
        
        if not files:
            QMessageBox.warning(self, "Warning", "No files found or invalid directory.")
            return
            
        prompt = self.prompt_input.toPlainText()
        if not prompt:
            QMessageBox.warning(self, "Warning", "Please enter a renaming instruction.")
            return
            
        sys_prompt, full_prompt = self.ai_renamer.construct_prompt(files, prompt)
        
        dialog = PromptPreviewDialog(sys_prompt, full_prompt, self)
        dialog.exec_()

    def preview_collapse(self):
        directory = self.collapse_dir_input.text()
        if not directory or not os.path.exists(directory):
            QMessageBox.warning(self, "Warning", "Invalid directory.")
            return
            
        try:
            redundant = identify_redundant_folders(directory)
            if not redundant:
                self.folder_results.setText("No redundant folders found.")
                return
                
            text = f"Found {len(redundant)} redundant folder structure(s):\n"
            for parent, child in redundant:
                text += f"{parent} -> {child}\n"
            self.folder_results.setText(text)
            self.collapse_preview_data = redundant
        except Exception as e:
            self.folder_results.setText(f"Error: {str(e)}")

    def apply_collapse(self):
        directory = self.collapse_dir_input.text()
        recursive = self.recursive_check.isChecked()
        
        if not directory or not os.path.exists(directory):
            QMessageBox.warning(self, "Warning", "Invalid directory.")
            return

        try:
            collapsed = collapse_redundant_folders(directory, recursive)
            if collapsed:
                text = f"Successfully collapsed {len(collapsed)} folder(s):\n"
                for folder in collapsed:
                    text += f"{folder}\n"
                self.folder_results.setText(text)
            else:
                self.folder_results.setText("No folders were collapsed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def preview_uncollapse(self):
        directory = self.uncollapse_dir_input.text()
        try:
            min_parts = int(self.min_parts_input.text())
        except ValueError:
            min_parts = 2
            
        if not directory or not os.path.exists(directory):
            QMessageBox.warning(self, "Warning", "Invalid directory.")
            return
            
        try:
            potential = []
            for item in os.listdir(directory):
                full_path = os.path.join(directory, item)
                if os.path.isdir(full_path) and len(item.split('_')) >= min_parts:
                    potential.append(full_path)
            
            if not potential:
                self.folder_results.setText(f"No folders found with {min_parts}+ parts.")
                return
                
            text = f"Found {len(potential)} folder(s) to uncollapse:\n"
            for folder in potential:
                name = os.path.basename(folder)
                parts = name.split('_')
                new_structure = ' -> '.join(parts)
                text += f"{name} -> [{new_structure}]\n"
            self.folder_results.setText(text)
        except Exception as e:
            self.folder_results.setText(f"Error: {str(e)}")

    def apply_uncollapse(self):
        directory = self.uncollapse_dir_input.text()
        try:
            min_parts = int(self.min_parts_input.text())
        except ValueError:
            min_parts = 2
            
        if not directory or not os.path.exists(directory):
            QMessageBox.warning(self, "Warning", "Invalid directory.")
            return

        try:
            uncollapsed = uncollapse_folders(directory, min_parts)
            if uncollapsed:
                text = f"Successfully uncollapsed {len(uncollapsed)} folder(s):\n"
                for folder in uncollapsed:
                    text += f"{folder}\n"
                self.folder_results.setText(text)
            else:
                self.folder_results.setText("No folders were uncollapsed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def toggle_regex_inputs(self, state):
        enabled = (state == Qt.Checked)
        self.regex_pattern_input.setEnabled(enabled)
        self.regex_repl_input.setEnabled(enabled)

def run_gui():
    app = QApplication(sys.argv)
    window = FileRenamerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_gui()
