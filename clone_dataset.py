#!/usr/bin/env python3
"""
Script to clone a Hugging Face dataset and set up git LFS for large file handling.
This script will clone the specified dataset, initialize git LFS, and set up upstream remote.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result."""
    print(f"Running command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(
        cmd,
        shell=isinstance(cmd, str),
        cwd=cwd,
        capture_output=True,
        text=True
    )
    
    if check and result.returncode != 0:
        print(f"Error running command: {result.stderr}")
        sys.exit(result.returncode)
    
    if result.stdout.strip():
        print(result.stdout)
    if result.stderr.strip():
        print(f"STDERR: {result.stderr}")
        
    return result


def main():
    parser = argparse.ArgumentParser(description="Clone Hugging Face dataset with git LFS")
    parser.add_argument("--dataset", required=True, help="Hugging Face dataset name (e.g., bwzheng2010/yahoo-finance-data)")
    parser.add_argument("--repo-name", required=True, help="Local repository name")
    
    args = parser.parse_args()
    
    # Clone the Hugging Face dataset
    hf_repo_url = f"https://huggingface.co/datasets/{args.dataset}"
    print(f"Cloning dataset from: {hf_repo_url}")
    
    clone_cmd = ["git", "clone", hf_repo_url, args.repo_name]
    run_command(clone_cmd)
    
    repo_path = Path(args.repo_name)
    
    # Initialize git LFS in the cloned repository
    print("Initializing git LFS...")
    run_command(["git", "lfs", "install"], cwd=repo_path)
    
    # Set up upstream remote
    print("Setting up upstream remote...")
    run_command(["git", "remote", "add", "upstream", hf_repo_url], cwd=repo_path)
    
    # Fetch from upstream to ensure we have the latest
    print("Fetching from upstream...")
    run_command(["git", "fetch", "upstream"], cwd=repo_path)
    
    print(f"Successfully cloned {args.dataset} to {args.repo_name} and set up git LFS with upstream remote.")
    print(f"Repository located at: {repo_path.absolute()}")


if __name__ == "__main__":
    main()