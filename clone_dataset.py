#!/usr/bin/env python3
"""
Script to clone a Hugging Face dataset and set it up with upstream tracking.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def load_env_vars():
    """Load environment variables from .env file."""
    load_dotenv()
    return os.getenv('HF_TOKEN')

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result."""
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    if check and result.returncode != 0:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(result.returncode)
    
    return result

def clone_hf_dataset(dataset_name, hf_token, target_dir):
    """Clone a Hugging Face dataset with git-lfs support."""
    print(f"Cloning dataset: {dataset_name}")
    
    # Create target directory if it doesn't exist
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    
    # Clone the dataset
    clone_url = f"https://hf.co/datasets/{dataset_name}"
    if hf_token:
        clone_url = f"https://{hf_token}@hf.co/datasets/{dataset_name}"
    
    cmd = ["git", "clone", clone_url, target_dir]
    run_command(cmd)
    
    # Initialize git lfs in the cloned repository
    print("Initializing git lfs...")
    run_command(["git", "lfs", "install"], cwd=target_dir)
    
    # Pull lfs files
    print("Pulling LFS files...")
    run_command(["git", "lfs", "pull"], cwd=target_dir)
    
    # Set the original repository as upstream
    print("Setting upstream to original repository...")
    run_command(["git", "remote", "add", "upstream", f"https://huggingface.co/datasets/{dataset_name}"], cwd=target_dir)
    
    # Fetch from upstream
    run_command(["git", "fetch", "upstream"], cwd=target_dir)
    
    print(f"Successfully cloned {dataset_name} to {target_dir} with upstream tracking")

def main():
    # Load HF token from environment
    hf_token = load_env_vars()
    
    if not hf_token:
        print("Error: HF_TOKEN not found in .env file")
        sys.exit(1)
    
    # Dataset name to clone
    dataset_name = "bwzheng2010/yahoo-finance-data"
    target_dir = "./data/hf_dataset"
    
    # Check if directory already exists
    if Path(target_dir).exists():
        print(f"Directory {target_dir} already exists. Skipping clone.")
        return
    
    clone_hf_dataset(dataset_name, hf_token, target_dir)

if __name__ == "__main__":
    main()