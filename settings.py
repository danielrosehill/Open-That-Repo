import json
import os
from pathlib import Path

class Settings:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/open-that-repo")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.default_git_base = os.path.expanduser("~/Git")
        self._ensure_config_dir()
        self.load_settings()

    def _ensure_config_dir(self):
        """Ensure the config directory exists"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def load_settings(self):
        """Load settings from config file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                'git_base_path': self.default_git_base
            }
            self.save_settings()

    def save_settings(self):
        """Save settings to config file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_git_base_path(self):
        """Get the base path for Git repositories"""
        return self.settings.get('git_base_path', self.default_git_base)

    def set_git_base_path(self, path):
        """Set the base path for Git repositories"""
        self.settings['git_base_path'] = path
        self.save_settings()
