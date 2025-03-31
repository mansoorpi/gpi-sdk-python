#!/usr/bin/env python3
"""
Backup script for GPI project.
Creates a timestamped zip archive of the current state.
"""

import os
import zipfile
import datetime
import sys
import shutil

def create_backup(base_dir='.', backup_dir='./backups'):
    """Create a backup of the GPI project."""
    # Create timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"gpi_backup_{timestamp}.zip"
    
    # Ensure backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Files/directories to exclude
    exclude = [
        '__pycache__', 
        '.git', 
        'backups',
        '.pytest_cache',
        '*.pyc',
        '*.pyo',
        '*.zip'
    ]
    
    def should_exclude(path):
        """Check if a path should be excluded from backup."""
        path = os.path.basename(path)
        for pattern in exclude:
            if pattern.startswith('*'):
                if path.endswith(pattern[1:]):
                    return True
            elif path == pattern:
                return True
        return False
    
    print(f"Creating backup at: {backup_path}")
    
    # Create zip file
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through directory
        for root, dirs, files in os.walk(base_dir):
            # Filter directories
            dirs[:] = [d for d in dirs if not should_exclude(d)]
            
            # Add files
            for file in files:
                if should_exclude(file) or file == backup_filename:
                    continue
                
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, base_dir)
                
                try:
                    zipf.write(file_path, arc_name)
                except Exception as e:
                    print(f"Error adding {file_path}: {e}")
    
    print(f"Backup created successfully: {backup_path}")
    print(f"Size: {os.path.getsize(backup_path) / (1024*1024):.2f} MB")
    return backup_path

if __name__ == "__main__":
    try:
        backup_path = create_backup()
        print(f"\nBackup complete. You can continue tomorrow with your project.")
        print(f"To restore: simply unzip {os.path.basename(backup_path)} in your project directory")
    except Exception as e:
        print(f"Backup failed: {e}")
        sys.exit(1) 