#!/usr/bin/env python3
"""
Optimized script to sync data from Hugging Face dataset to local repository
This script properly handles Git LFS pointers instead of copying raw large files
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file in parent directory"""
    env_path = Path(__file__).parent / ".." / ".env"  # Look in parent directory as requested
    load_dotenv(dotenv_path=env_path)
    return os.getenv('HF_TOKEN')


def run_command(cmd, cwd=None, check=True, capture_output=True):
    """Run a shell command and return the result"""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            cwd=cwd,
            check=check,
            capture_output=capture_output,
            text=True
        )
        if result.stdout and capture_output:
            print(f"  stdout: {result.stdout.strip()}")
        if result.stderr and capture_output:
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
    """Setup upstream and target remotes"""
    print("Setting up remotes...")

    # Remove any existing remotes to avoid conflicts
    run_command(["git", "remote", "remove", "upstream"], check=False)
    run_command(["git", "remote", "remove", "target"], check=False)

    # Add upstream remote (source dataset)
    upstream_url = "https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data"
    run_command(["git", "remote", "add", "upstream", upstream_url])

    # Add target remote (your Hugging Face dataset)
    target_username = "richard-chau"  # This should be updated to your actual username
    target_url = f"https://{target_username}:{hf_token}@huggingface.co/datasets/{target_username}/yahoo-finance-data"
    run_command(["git", "remote", "add", "target", target_url])

    print(f"Upstream remote added: {upstream_url}")
    print(f"Target remote added: {target_url}")


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


def push_to_github():
    """Push changes to the origin repository (GitHub)"""
    print("Checking for changes to push to GitHub...")
    status_output = run_command(["git", "status", "--porcelain"])

    if status_output and status_output.strip():
        print("Changes detected, committing and pushing to GitHub...")

        # Add all changes
        run_command(["git", "add", "."])

        # Commit changes
        run_command(["git", "commit", "-m", "Auto-sync from upstream HF dataset [skip ci]"])

        # Push to origin (GitHub)
        run_command(["git", "push", "origin", "main"])

        print("Successfully pushed changes to GitHub.")
    else:
        print("No changes to commit to GitHub.")


def push_to_huggingface(hf_token):
    """Push changes to your Hugging Face dataset repository"""
    print("Checking if target remote exists...")
    remotes = run_command(["git", "remote", "-v"])

    if "target" in remotes:
        print("Pushing changes to Hugging Face...")

        # Push to target (Hugging Face)
        run_command(["git", "push", "target", "main", "--force"])

        print("Successfully pushed changes to Hugging Face.")
    else:
        print("Target remote not found. Skipping Hugging Face push.")


def main():
    """Main function to orchestrate the sync process"""
    print("Starting optimized Hugging Face dataset sync...")

    # Load HF token from ../.env as requested
    hf_token = load_env()
    if not hf_token or hf_token == "your_actual_token_here":
        print("Error: HF_TOKEN not found in ../.env file or still set to default value")
        print("Please update the ../.env file with your actual Hugging Face token")
        sys.exit(1)

    print("HF_TOKEN loaded successfully from ../.env")

    # Initialize Git LFS
    initialize_git_lfs()

    # Setup git configuration
    setup_git_config()

    # Setup remotes
    setup_remotes(hf_token)

    # Sync data from upstream
    sync_from_upstream()

    # Push changes to GitHub
    push_to_github()

    # Push changes to Hugging Face
    push_to_huggingface(hf_token)

    print("Hugging Face dataset sync completed successfully!")


if __name__ == "__main__":
    main()