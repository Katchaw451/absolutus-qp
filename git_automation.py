#!/usr/bin/env python3
"""
FCTUC Security System - Git Automation
Auto-commits and pushes security scripts to GitHub
"""

import subprocess
import os
import datetime
import hashlib
import time

class GitAutomation:
    def __init__(self):
        self.username = "katchaw451"
        self.email = "katchaw451@gmail.com"
        self.repo_path = os.getcwd()
        self.security_files = [
            'security_dashboard.py',
            'git_automation.py', 
            'network_defender.py',
            'access_control.py',
            'threat_analyzer.py'
        ]
        
    def setup_git_config(self):
        """Configure git user settings"""
        try:
            subprocess.run(['git', 'config', 'user.name', self.username], check=True)
            subprocess.run(['git', 'config', 'user.email', self.email], check=True)
            print("✅ Git configuration set")
        except subprocess.CalledProcessError as e:
            print(f"❌ Git config error: {e}")
            
    def get_file_checksum(self, filename):
        """Calculate file checksum for change detection"""
        if not os.path.exists(filename):
            return None
        with open(filename, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def check_for_changes(self):
        """Check if any security files have changed"""
        changes = []
        for file in self.security_files:
            if os.path.exists(file):
                # Check if file is modified
                result = subprocess.run(['git', 'status', '--porcelain', file], 
                                      capture_output=True, text=True)
                if result.stdout.strip():
                    changes.append(file)
        return changes
    
    def commit_and_push(self, commit_message=None):
        """Commit and push changes to GitHub"""
        if not commit_message:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Security System Update - {timestamp}"
        
        try:
            # Add all security files
            for file in self.security_files:
                if os.path.exists(file):
                    subprocess.run(['git', 'add', file], check=True)
            
            # Commit
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # Push to main branch
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            
            print(f"✅ Successfully pushed: {commit_message}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            return False
    
    def initialize_repo(self):
        """Initialize git repository if not exists"""
        if not os.path.exists('.git'):
            try:
                subprocess.run(['git', 'init'], check=True)
                print("✅ Git repository initialized")
            except subprocess.CalledProcessError as e:
                print(f"❌ Git init failed: {e}")
                return False
        return True
    
    def auto_commit_loop(self, interval=300):
        """Automatically commit changes at intervals"""
        print("🔄 Starting auto-commit service...")
        print(f"⏰ Commit interval: {interval} seconds")
        
        while True:
            try:
                changes = self.check_for_changes()
                if changes:
                    print(f"📁 Detected changes in: {', '.join(changes)}")
                    self.commit_and_push()
                else:
                    print("📊 No changes detected")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Auto-commit service stopped")
                break
            except Exception as e:
                print(f"❌ Auto-commit error: {e}")
                time.sleep(60)  # Wait before retry

def main():
    git_auto = GitAutomation()
    
    print("🚀 FCTUC Security Git Automation")
    print("=" * 40)
    
    # Setup
    if git_auto.initialize_repo():
        git_auto.setup_git_config()
        
        # Manual commit or auto mode
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == '--auto':
            git_auto.auto_commit_loop()
        else:
            changes = git_auto.check_for_changes()
            if changes:
                print(f"Changes detected: {changes}")
                git_auto.commit_and_push()
            else:
                print("No changes to commit")

if __name__ == "__main__":
    main()
