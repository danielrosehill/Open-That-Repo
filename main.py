import os
import subprocess
import sys
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QMessageBox)
from PyQt6.QtCore import Qt
from settings import Settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Open That Repo')
        self.setMinimumWidth(600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Git base path section
        base_path_layout = QHBoxLayout()
        base_path_label = QLabel('Git Base Path:')
        self.base_path_input = QLineEdit(self.settings.get_git_base_path())
        base_path_save = QPushButton('Save')
        base_path_save.clicked.connect(self.save_base_path)
        
        base_path_layout.addWidget(base_path_label)
        base_path_layout.addWidget(self.base_path_input)
        base_path_layout.addWidget(base_path_save)
        layout.addLayout(base_path_layout)

        # GitHub URL section
        url_layout = QHBoxLayout()
        url_label = QLabel('GitHub URL:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('https://github.com/username/repo')
        find_button = QPushButton('Find Repo')
        find_button.clicked.connect(self.find_repo)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(find_button)
        layout.addLayout(url_layout)

        # Result section
        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.result_label)

        # Open in VS Code button (hidden by default)
        self.open_button = QPushButton('Open in VS Code')
        self.open_button.clicked.connect(self.open_in_vscode)
        self.open_button.hide()
        layout.addWidget(self.open_button)

        layout.addStretch()

    def save_base_path(self):
        path = self.base_path_input.text()
        if os.path.exists(path):
            self.settings.set_git_base_path(path)
            QMessageBox.information(self, 'Success', 'Git base path saved successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Invalid path. Please enter a valid directory path.')

    def find_repo(self):
        url = self.url_input.text().strip()
        if not url.startswith('https://github.com/'):
            QMessageBox.warning(self, 'Error', 'Please enter a valid GitHub URL')
            return

        # Extract repo name from URL
        repo_name = url.split('/')[-1]
        base_path = Path(self.settings.get_git_base_path())
        
        found_repo = None
        
        # Search through directories
        for root, dirs, _ in os.walk(base_path):
            if '.git' in dirs:
                git_dir = Path(root) / '.git'
                try:
                    # Check if this is the repo we're looking for
                    config_file = git_dir / 'config'
                    if config_file.exists():
                        with open(config_file, 'r') as f:
                            config_content = f.read()
                            if url in config_content or f"{url}.git" in config_content:
                                # Verify this is not a submodule
                                if not any(p.name == '.git' for p in Path(root).parents):
                                    found_repo = root
                                    break
                except Exception as e:
                    print(f"Error reading git config: {e}")

        if found_repo:
            self.result_label.setText(f'Repository found at: {found_repo}')
            self.found_repo_path = found_repo
            self.open_button.show()
        else:
            self.result_label.setText('Repository not found in the specified base path.')
            self.open_button.hide()

    def open_in_vscode(self):
        try:
            subprocess.Popen(['code', self.found_repo_path])
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to open VS Code: {str(e)}')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
