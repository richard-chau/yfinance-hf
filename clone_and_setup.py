#!/usr/bin/env python3
"""
Script to clone a Hugging Face dataset, initialize git-lfs,
and set up upstream tracking for daily synchronization.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from dotenv import load_dotenv


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
    
    return result


def load_token_from_env():
    """Load HF token from ../.env file."""
    env_path = Path("../.env").resolve()
    load_dotenv(env_path)
    
    hf_token = os.getenv('HF_TOKEN')
    if not hf_token:
        raise ValueError(f"HF_TOKEN not found in {env_path}")
    
    return hf_token


def clone_dataset(dataset_url, target_dir, hf_token):
    """Clone the Hugging Face dataset."""
    print(f"Cloning dataset from {dataset_url} to {target_dir}")
    
    # Clone with git-lfs support
    clone_cmd = [
        "git", "clone", f"https://hf_{hf_token}@huggingface.co/datasets/{dataset_url}", 
        target_dir
    ]
    run_command(clone_cmd)
    
    # Initialize git-lfs in the cloned repository
    print("Initializing git-lfs...")
    run_command(["git", "lfs", "install"], cwd=target_dir)
    
    # Pull LFS files
    print("Pulling LFS files...")
    run_command(["git", "lfs", "pull"], cwd=target_dir)


def setup_upstream_tracking(target_dir, dataset_url, hf_token):
    """Set up upstream tracking for the dataset."""
    print("Setting up upstream tracking...")
    
    # Add upstream remote
    upstream_url = f"https://hf_{hf_token}@huggingface.co/datasets/{dataset_url}"
    run_command(["git", "remote", "add", "upstream", upstream_url], cwd=target_dir)
    
    # Verify remotes
    result = run_command(["git", "remote", "-v"], cwd=target_dir)
    print("Current remotes:")
    print(result.stdout)


def main():
    parser = argparse.ArgumentParser(description="Clone Hugging Face dataset and set up upstream tracking")
    parser.add_argument("--dataset", required=True, help="Dataset name (e.g., username/dataset-name)")
    parser.add_argument("--target-dir", required=True, help="Target directory to clone to")
    
    args = parser.parse_args()
    
    # Load token from .env file
    hf_token = load_token_from_env()
    print(f"Using HF token from ../.env file")
    
    # Create target directory if it doesn't exist
    target_path = Path(args.target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Clone the dataset
    clone_dataset(args.dataset, args.target_dir, hf_token)
    
    # Set up upstream tracking
    setup_upstream_tracking(args.target_dir, args.dataset, hf_token)
    
    print(f"\nSuccessfully cloned {args.dataset} to {args.target_dir}")
    print(f"Upstream tracking set up for https://huggingface.co/datasets/{args.dataset}")
    print("\nTo sync with upstream later, run:")
    print(f"  cd {args.target_dir}")
    print("  git fetch upstream")
    print("  git merge upstream/main -X theirs")


if __name__ == "__main__":
    main()