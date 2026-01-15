#!/usr/bin/env python3
"""
Script to clone a Hugging Face dataset, initialize git-lfs, and set upstream tracking.
"""

import os
import subprocess
import sys
from pathlib import Path

def load_env_vars():
    """Load environment variables from .env file."""
    env_path = Path("../.env")
    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        return None
    
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars

def run_command(cmd, cwd=None, env_vars=None):
    """Run a shell command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    try:
        # Merge environment variables if provided
        env = os.environ.copy()
        if env_vars:
            env.update(env_vars)
        
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        if result.returncode != 0:
            print(f"Error running command: {' '.join(cmd)}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
            return False, result.stdout, result.stderr
        
        print(f"Success: {result.stdout}")
        return True, result.stdout, result.stderr
    except Exception as e:
        print(f"Exception running command: {' '.join(cmd)} - {str(e)}")
        return False, "", str(e)

def main():
    print("Starting Hugging Face dataset cloning process...")
    
    # Load environment variables
    env_vars = load_env_vars()
    if not env_vars:
        print("Failed to load environment variables from .env file.")
        sys.exit(1)
    
    hf_token = env_vars.get("HF_TOKEN")
    if not hf_token or hf_token == "your_actual_token_here":
        print("Error: HF_TOKEN not found or still set to default value in .env file.")
        print("Please update your .env file with a valid Hugging Face token.")
        sys.exit(1)
    
    # Dataset information
    dataset_name = "bwzheng2010/yahoo-finance-data"
    repo_url = f"https://huggingface.co/datasets/{dataset_name}"
    
    # Clone the dataset
    print(f"\nCloning dataset from: {repo_url}")
    success, _, _ = run_command([
        "git", "clone", f"https://{hf_token}@huggingface.co/datasets/{dataset_name}", "yahoo-finance-data"
    ])
    
    if not success:
        print("Failed to clone the dataset.")
        sys.exit(1)
    
    # Change to the dataset directory
    dataset_dir = Path("yahoo-finance-data")
    
    # Initialize git-lfs in the cloned repository
    print("\nInitializing git-lfs...")
    success, _, _ = run_command(["git", "lfs", "install"], cwd=dataset_dir)
    if not success:
        print("Failed to initialize git-lfs.")
        sys.exit(1)
    
    # Set the original Hugging Face repo as upstream
    print("\nSetting upstream remote...")
    success, _, _ = run_command([
        "git", "remote", "add", "upstream", f"https://huggingface.co/datasets/{dataset_name}"
    ], cwd=dataset_dir)
    
    if not success:
        # Check if upstream already exists
        success_check, _, _ = run_command(["git", "remote", "-v"], cwd=dataset_dir)
        if success_check:
            print("Upstream remote may already exist.")
        else:
            print("Failed to set upstream remote.")
            sys.exit(1)
    
    # Fetch from upstream to ensure we have the latest
    print("\nFetching from upstream...")
    success, _, _ = run_command(["git", "fetch", "upstream"], cwd=dataset_dir)
    if not success:
        print("Failed to fetch from upstream.")
        sys.exit(1)
    
    print(f"\nDataset successfully cloned to {dataset_dir}")
    print("Git LFS initialized and upstream remote set.")
    print("You can now pull updates from upstream using: git pull upstream main")

if __name__ == "__main__":
    main()