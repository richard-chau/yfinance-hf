#!/usr/bin/env python3
"""
Script to clone a Hugging Face dataset, initialize git-lfs,
and set up upstream remote for daily synchronization.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        return os.getenv('HF_TOKEN')
    else:
        print(f"Warning: .env file not found at {env_path}")
        return None


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result."""
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
    
    print(f"stdout: {result.stdout}")
    if result.stderr:
        print(f"stderr: {result.stderr}")
    
    return result


def clone_dataset(dataset_repo_url, target_dir):
    """Clone the Hugging Face dataset repository."""
    print(f"Cloning dataset from {dataset_repo_url} to {target_dir}")
    
    # Clone the repository with git-lfs support
    run_command(['git', 'clone', dataset_repo_url, target_dir])
    
    # Initialize git-lfs in the cloned repository
    print("Initializing git-lfs...")
    run_command(['git', 'lfs', 'install'], cwd=target_dir)


def setup_upstream_remote(target_dir, upstream_repo_url):
    """Set up the upstream remote for synchronization."""
    print(f"Setting up upstream remote: {upstream_repo_url}")
    run_command(['git', 'remote', 'add', 'upstream', upstream_repo_url], cwd=target_dir)
    
    # Fetch from upstream to establish the connection
    run_command(['git', 'fetch', 'upstream'], cwd=target_dir)
    
    print("Upstream remote configured successfully!")


def main():
    # Load HF token from .env
    hf_token = load_env()
    
    if not hf_token or hf_token == "your_actual_token_here":
        print("Warning: HF_TOKEN not properly set in .env file.")
        print("Please get your token from https://huggingface.co/settings/tokens")
        print("and replace 'your_actual_token_here' in the .env file.")
        hf_token_input = input("Alternatively, enter your HF token now (or press Enter to skip): ").strip()
        if hf_token_input:
            hf_token = hf_token_input
    
    # Dataset information
    dataset_name = "bwzheng2010/yahoo-finance-data"
    dataset_repo_url = f"https://{hf_token}@huggingface.co/datasets/{dataset_name}"
    target_dir = "data"
    
    # Clone the dataset
    clone_dataset(dataset_repo_url, target_dir)
    
    # Set up upstream remote pointing to the original dataset
    upstream_repo_url = f"https://huggingface.co/datasets/{dataset_name}"
    setup_upstream_remote(target_dir, upstream_repo_url)
    
    print("\nDataset cloned and upstream remote configured successfully!")
    print(f"Repository located at: {os.path.abspath(target_dir)}")
    print("You can now set up GitHub Actions for daily synchronization.")


if __name__ == "__main__":
    main()