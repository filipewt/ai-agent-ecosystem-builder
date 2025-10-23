"""
Backup & Version Control Agent - Manages backups and version control
"""

import os
import shutil
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class BackupAgent(BaseAgent):
    """Agent responsible for backup and version control"""
    
    def __init__(self):
        super().__init__(
            agent_id="backup_001",
            name="Backup & Version Control Agent",
            description="Creates backups and manages version control"
        )
        self.backup_dir = "backups"
        self.backup_history = []
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute backup operations"""
        try:
            self.log_action("Starting backup operations")
            
            # Create backup directory
            self._ensure_backup_dir()
            
            # Get files to backup
            files_to_backup = context.get("generated_files", [])
            if not files_to_backup:
                return self.create_response(
                    False,
                    "No files provided for backup"
                )
            
            # Create backup
            backup_path = self._create_backup(files_to_backup)
            
            # Update backup history
            self._update_backup_history(backup_path, files_to_backup)
            
            self.log_action("Backup operations completed")
            return self.create_response(
                True,
                "🗃️ Backup created successfully",
                {"backup_path": backup_path, "files_backed_up": files_to_backup}
            )
            
        except Exception as e:
            self.logger.error(f"Backup operations failed: {str(e)}")
            return self.create_response(False, f"Backup operations failed: {str(e)}")
    
    def _ensure_backup_dir(self):
        """Ensure backup directory exists"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            self.logger.info(f"Created backup directory: {self.backup_dir}")
    
    def _create_backup(self, files: List[str]) -> str:
        """Create backup of files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
        
        # Create backup directory
        os.makedirs(backup_path, exist_ok=True)
        
        # Copy files to backup
        for file_path in files:
            if os.path.exists(file_path):
                # Create directory structure in backup
                rel_path = os.path.relpath(file_path)
                backup_file_path = os.path.join(backup_path, rel_path)
                backup_file_dir = os.path.dirname(backup_file_path)
                
                if backup_file_dir:
                    os.makedirs(backup_file_dir, exist_ok=True)
                
                shutil.copy2(file_path, backup_file_path)
                self.logger.info(f"Backed up: {file_path} -> {backup_file_path}")
        
        # Create backup metadata
        metadata = {
            "timestamp": timestamp,
            "files": files,
            "backup_path": backup_path,
            "created_by": self.agent_id
        }
        
        with open(os.path.join(backup_path, "backup_metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
        
        return backup_path
    
    def _update_backup_history(self, backup_path: str, files: List[str]):
        """Update backup history"""
        backup_entry = {
            "timestamp": datetime.now().isoformat(),
            "backup_path": backup_path,
            "files": files,
            "agent_id": self.agent_id
        }
        
        self.backup_history.append(backup_entry)
        
        # Save history to file
        history_file = os.path.join(self.backup_dir, "backup_history.json")
        with open(history_file, "w") as f:
            json.dump(self.backup_history, f, indent=2)
    
    def restore_from_backup(self, backup_path: str) -> Dict[str, Any]:
        """Restore files from backup"""
        try:
            if not os.path.exists(backup_path):
                return self.create_response(
                    False,
                    f"Backup path not found: {backup_path}"
                )
            
            # Load backup metadata
            metadata_file = os.path.join(backup_path, "backup_metadata.json")
            if not os.path.exists(metadata_file):
                return self.create_response(
                    False,
                    "Backup metadata not found"
                )
            
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            
            # Restore files
            restored_files = []
            for file_path in metadata["files"]:
                backup_file_path = os.path.join(backup_path, os.path.relpath(file_path))
                if os.path.exists(backup_file_path):
                    shutil.copy2(backup_file_path, file_path)
                    restored_files.append(file_path)
            
            self.log_action(f"Restored {len(restored_files)} files from backup")
            return self.create_response(
                True,
                f"Restored {len(restored_files)} files from backup",
                {"restored_files": restored_files}
            )
            
        except Exception as e:
            self.logger.error(f"Restore failed: {str(e)}")
            return self.create_response(False, f"Restore failed: {str(e)}")
    
    def get_backup_history(self) -> List[Dict[str, Any]]:
        """Get backup history"""
        return self.backup_history
    
    def cleanup_old_backups(self, keep_count: int = 5) -> Dict[str, Any]:
        """Clean up old backups, keeping only the most recent ones"""
        try:
            if len(self.backup_history) <= keep_count:
                return self.create_response(
                    True,
                    "No cleanup needed",
                    {"backups_kept": len(self.backup_history)}
                )
            
            # Sort backups by timestamp
            sorted_backups = sorted(
                self.backup_history,
                key=lambda x: x["timestamp"],
                reverse=True
            )
            
            # Keep only the most recent backups
            backups_to_keep = sorted_backups[:keep_count]
            backups_to_remove = sorted_backups[keep_count:]
            
            # Remove old backups
            removed_count = 0
            for backup in backups_to_remove:
                backup_path = backup["backup_path"]
                if os.path.exists(backup_path):
                    shutil.rmtree(backup_path)
                    removed_count += 1
            
            # Update history
            self.backup_history = backups_to_keep
            
            self.log_action(f"Cleaned up {removed_count} old backups")
            return self.create_response(
                True,
                f"Cleaned up {removed_count} old backups",
                {"backups_kept": len(backups_to_keep), "backups_removed": removed_count}
            )
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")
            return self.create_response(False, f"Cleanup failed: {str(e)}")
