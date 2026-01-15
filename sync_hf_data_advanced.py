#!/usr/bin/env python3
"""
Advanced script to sync data from Hugging Face dataset to local repository
Handles Git LFS properly and manages the sync process
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from dotenv import load_dotenv

def load_env_vars():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / ".." / ".env"
    load_dotenv(env_path)
    return os.getenv('HF_TOKEN')

def run_command(cmd, cwd=None, capture_output=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd,
            capture_output=capture_output, 
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error output: {e.stderr}")
        raise e

def initialize_git_lfs(repo_path):
    """Initialize Git LFS in the repository"""
    print("Initializing Git LFS...")
    run_command("git lfs install", cwd=repo_path)
    print("Git LFS initialized successfully.")

def setup_remotes(repo_path, hf_token, source_repo, target_repo_name):
    """Setup source and target remotes"""
    print(f"Setting up source remote: {source_repo}")
    run_command(f"git remote remove upstream", cwd=repo_path, capture_output=False)
    run_command(f"git remote add upstream {source_repo}", cwd=repo_path, capture_output=False)
    
    print(f"Setting up target remote: {target_repo_name}")
    target_url = f"https://{os.getenv('GITHUB_ACTOR')}:{hf_token}@huggingface.co/datasets/{target_repo_name}"
    run_command(f"git remote remove target", cwd=repo_path, capture_output=False)
    run_command(f"git remote add target {target_url}", cwd=repo_path, capture_output=False)

def sync_data(repo_path):
    """Sync data from upstream to target"""
    print("Fetching upstream data...")
    run_command("git fetch upstream main", cwd=repo_path, capture_output=False)
    
    print("Merging upstream data (using theirs in case of conflicts)...")
    run_command("git merge upstream/main -m 'Auto-sync from upstream' -X ours", cwd=repo_path, capture_output=False)
    
    print("Sync completed successfully!")

def push_to_target(repo_path):
    """Push synced data to target repository"""
    print("Pushing to target repository...")
    run_command("git push target main --force", cwd=repo_path, capture_output=False)
    print("Data pushed to target successfully!")

def main():
    # Load environment variables
    hf_token = load_env_vars()
    if not hf_token or hf_token == "your_actual_token_here":
        print("Error: HF_TOKEN not found in .env file or still has default value")
        print("Please update your .env file with a valid Hugging Face token")
        print("Get your token from https://huggingface.co/settings/tokens")
        sys.exit(1)
    
    # Configuration
    source_repo = "https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data"
    target_repo_name = f"{os.getenv('GITHUB_ACTOR')}/yahoo-finance-data"
    repo_path = os.getcwd()  # Current directory
    
    # Initialize Git LFS
    initialize_git_lfs(repo_path)
    
    # Setup remotes
    setup_remotes(repo_path, hf_token, source_repo, target_repo_name)
    
    # Sync data
    sync_data(repo_path)
    
    # Push to target
    push_to_target(repo_path)
    
    print("\nSync process completed successfully!")

if __name__ == "__main__":
    main()