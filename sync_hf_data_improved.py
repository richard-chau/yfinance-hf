#!/usr/bin/env python3
"""
Improved script to sync data from Hugging Face dataset to local repository
This script properly handles Git LFS pointers instead of copying raw large files
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)
    return os.getenv('HF_TOKEN')


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result"""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print(f"  stdout: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"  stderr: {result.stderr.strip()}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"  Error running command: {e}")
        print(f"  Stderr: {e.stderr}")
        if check:
            raise
        return None


def initialize_git_lfs():
    """Initialize Git LFS for handling large files"""
    print("Initializing Git LFS...")
    run_command(["git", "lfs", "install"])
    print("Git LFS initialized successfully.")


def setup_git_config():
    """Configure git user information"""
    print("Setting up git configuration...")
    run_command(["git", "config", "user.name", "richard-chau"])
    run_command(["git", "config", "user.email", "richard.chau@example.com"])
    print("Git configuration completed.")


def setup_remotes(hf_token):
    """Setup upstream remote for the source dataset"""
    print("Setting up remotes...")

    # Remove any existing upstream remote to avoid conflicts
    run_command(["git", "remote", "remove", "upstream"], check=False)
    
    # Add upstream remote (source dataset)
    upstream_url = "https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data"
    run_command(["git", "remote", "add", "upstream", upstream_url])
    
    print(f"Upstream remote added: {upstream_url}")


def sync_from_upstream():
    """Sync data from upstream to local repository"""
    print("Fetching upstream data...")
    run_command(["git", "fetch", "upstream", "main"])

    print("Getting current branch...")
    current_branch = run_command(["git", "branch", "--show-current"]).strip()
    
    print(f"Merging upstream data into {current_branch}...")
    # Merge with strategy to prefer upstream changes in case of conflicts
    run_command([
        "git", "merge", "upstream/main", 
        "-m", "Auto-sync from bwzheng2010 [skip ci]", 
        "-X", "theirs", 
        "--allow-unrelated-histories"
    ])

    print("Sync from upstream completed successfully.")


def push_to_origin():
    """Push changes to the origin repository (GitHub)"""
    print("Checking for changes...")
    status_output = run_command(["git", "status", "--porcelain"])

    if status_output.strip():
        print("Changes detected, committing and pushing...")
        
        # Add all changes
        run_command(["git", "add", "."])
        
        # Commit changes
        run_command(["git", "commit", "-m", "Auto-sync from upstream HF dataset [skip ci]"])
        
        # Push to origin
        run_command(["git", "push", "origin", "main"])
        
        print("Successfully pushed changes to origin.")
    else:
        print("No changes to commit.")


def main():
    """Main function to orchestrate the sync process"""
    print("Starting Hugging Face dataset sync (improved version)...")

    # Load HF token from .env
    hf_token = load_env()
    if not hf_token or hf_token == "your_actual_token_here":
        print("Error: HF_TOKEN not found in .env file or still set to default value")
        print("Please update the .env file with your actual Hugging Face token")
        sys.exit(1)

    print("HF_TOKEN loaded successfully")

    # Initialize Git LFS
    initialize_git_lfs()

    # Setup git configuration
    setup_git_config()

    # Setup remotes
    setup_remotes(hf_token)

    # Sync data from upstream
    sync_from_upstream()

    # Push changes to origin (GitHub)
    push_to_origin()

    print("Hugging Face dataset sync completed successfully!")


if __name__ == "__main__":
    main()