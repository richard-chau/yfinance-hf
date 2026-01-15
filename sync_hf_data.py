#!/usr/bin/env python3
"""
Script to sync data from Hugging Face dataset to local repository
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / ".." / ".env"
    load_dotenv(dotenv_path=env_path)
    return os.getenv('HF_TOKEN')

def run_command(cmd, cwd=None):
    """Run a shell command and return the result"""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Stderr: {e.stderr}")
        raise

def initialize_git_lfs():
    """Initialize Git LFS for handling large files"""
    print("Initializing Git LFS...")
    run_command(["git", "lfs", "install"])
    print("Git LFS initialized successfully.")

def setup_remotes(hf_token):
    """Setup upstream and target remotes"""
    print("Setting up remotes...")
    
    # Add upstream remote (source dataset)
    run_command(["git", "remote", "add", "upstream", "https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data"])
    
    # Add target remote (your dataset)
    target_url = f"https://hf.co/datasets/winterandchaiyun/yahoo-finance-data"
    run_command(["git", "remote", "set-url", "origin", target_url])
    
    print("Remotes configured successfully.")

def sync_data():
    """Sync data from upstream to local repository"""
    print("Fetching upstream data...")
    run_command(["git", "fetch", "upstream", "main"])
    
    print("Merging upstream data...")
    # Merge with strategy to prefer upstream changes in case of conflicts
    run_command(["git", "merge", "upstream/main", "-m", "Auto-sync from bwzheng2010", "-X", "theirs"])
    
    print("Sync completed successfully.")

def commit_and_push(hf_token):
    """Commit changes and push to target repository"""
    print("Configuring git user...")
    run_command(["git", "config", "user.name", "winterandchaiyun"])
    run_command(["git", "config", "user.email", "alex.zhou@example.com"])
    
    print("Adding files...")
    run_command(["git", "add", "."])
    
    print("Checking for changes...")
    status_output = run_command(["git", "status", "--porcelain"])
    
    if status_output.strip():
        print("Changes detected, committing...")
        run_command(["git", "commit", "-m", "Auto-sync from upstream HF dataset"])
        
        print("Pushing to target repository...")
        run_command(["git", "push", "origin", "main", "--force"])
        print("Successfully pushed to target repository.")
    else:
        print("No changes to commit.")

def main():
    """Main function to orchestrate the sync process"""
    print("Starting Hugging Face dataset sync...")
    
    # Load HF token from .env
    hf_token = load_env()
    if not hf_token or hf_token == "your_actual_token_here":
        print("Error: HF_TOKEN not found in .env file or still set to default value")
        print("Please update the .env file with your actual Hugging Face token")
        sys.exit(1)
    
    print("HF_TOKEN loaded successfully")
    
    # Initialize Git LFS
    initialize_git_lfs()
    
    # Setup remotes
    setup_remotes(hf_token)
    
    # Sync data from upstream
    sync_data()
    
    # Commit and push changes
    commit_and_push(hf_token)
    
    print("Hugging Face dataset sync completed successfully!")

if __name__ == "__main__":
    main()