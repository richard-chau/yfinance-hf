#!/usr/bin/env python3
"""
Script to sync data from Hugging Face dataset to local repository
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result"""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(
        cmd,
        shell=isinstance(cmd, str),
        cwd=cwd,
        capture_output=True,
        text=True
    )
    
    if check and result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(result.returncode)
    
    return result

def initialize_git_lfs():
    """Initialize Git LFS in the repository"""
    print("Initializing Git LFS...")
    run_command(["git", "lfs", "install"])
    print("Git LFS initialized successfully.")

def sync_from_upstream(repo_url, branch="main"):
    """Sync data from upstream Hugging Face dataset"""
    print(f"Syncing from upstream: {repo_url}")
    
    # Add upstream remote if it doesn't exist
    remotes_result = run_command(["git", "remote", "-v"], check=False)
    if "upstream" not in remotes_result.stdout:
        print("Adding upstream remote...")
        run_command(["git", "remote", "add", "upstream", repo_url])
    
    # Fetch from upstream
    print("Fetching from upstream...")
    run_command(["git", "fetch", "upstream", branch])
    
    # Merge upstream changes (with theirs taking precedence in case of conflicts)
    print("Merging upstream changes...")
    run_command([
        "git", "merge", f"upstream/{branch}", 
        "-m", "Sync: Update from upstream", 
        "--allow-unrelated-histories", 
        "-X", "theirs"
    ])
    
    print("Successfully synced from upstream!")

def push_to_target(target_repo_url, branch="main"):
    """Push the synced data to the target repository"""
    print(f"Pushing to target: {target_repo_url}")

    # Add target remote if it doesn't exist
    remotes_result = run_command(["git", "remote", "-v"], check=False)
    if "target" not in remotes_result.stdout:
        print("Adding target remote...")
        run_command(["git", "remote", "add", "target", target_repo_url])

    # Push to target
    print("Pushing to target...")
    run_command(["git", "push", "target", branch, "--force"])

    # Also push LFS objects
    print("Pushing LFS objects...")
    run_command(["git", "lfs", "push", "target", branch])

    print("Successfully pushed to target!")

def main():
    # Load HF token from .env file
    from dotenv import load_dotenv
    load_dotenv('../.env')  # Load from parent directory
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token or hf_token == "your_actual_token_here":
        print("Error: HF_TOKEN not properly set in .env file!")
        print("Please update the HF_TOKEN in ../.env with your actual Hugging Face token")
        sys.exit(1)
    
    # Initialize Git LFS
    initialize_git_lfs()
    
    # Upstream repository (source)
    upstream_repo = "https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data"
    
    # Target repository (destination) - replace with your actual HF username/repo
    # For now, we'll use the same repo as upstream, but you should change this to your own
    target_repo = f"https://hf_username:{hf_token}@huggingface.co/datasets/hf_username/yahoo-finance-data"
    
    # Perform sync
    sync_from_upstream(upstream_repo)
    push_to_target(target_repo)
    
    print("Sync completed successfully!")

if __name__ == "__main__":
    main()