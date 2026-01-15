#!/usr/bin/env python3
"""
Script to clone a Hugging Face dataset and set up upstream tracking
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def load_hf_token():
    """Load HF token from .env file"""
    load_dotenv('../.env')
    hf_token = os.getenv('HF_TOKEN')
    
    if not hf_token:
        print("Error: HF_TOKEN not found in ../.env file")
        print("Please add your Hugging Face token to the .env file")
        sys.exit(1)
        
    return hf_token

def run_command(cmd, cwd=None):
    """Run a shell command and handle errors"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Command '{cmd}' executed successfully")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{cmd}': {e.stderr}")
        sys.exit(1)

def main():
    # Load HF token
    hf_token = load_hf_token()
    
    # Define dataset info
    dataset_name = "bwzheng2010/yahoo-finance-data"
    dataset_url = f"https://huggingface.co/datasets/{dataset_name}"
    repo_url_with_token = f"https://{hf_token}@huggingface.co/datasets/{dataset_name}.git"
    
    # Create datasets directory if it doesn't exist
    datasets_dir = Path("datasets")
    datasets_dir.mkdir(exist_ok=True)
    
    # Clone the dataset
    dataset_dir = datasets_dir / dataset_name.split('/')[-1]
    
    if dataset_dir.exists():
        print(f"Dataset directory {dataset_dir} already exists, pulling latest changes...")
        run_command("git pull origin main", cwd=dataset_dir)
    else:
        print(f"Cloning dataset from {dataset_url}...")
        run_command(f"git clone {repo_url_with_token} {dataset_dir}")
    
    # Initialize git lfs
    print("Initializing Git LFS...")
    run_command("git lfs install", cwd=dataset_dir)
    
    # Pull LFS files
    print("Pulling LFS files...")
    run_command("git lfs pull", cwd=dataset_dir)
    
    # Set the original Hugging Face repo as upstream
    print("Setting upstream to original Hugging Face dataset...")
    run_command(f"git remote add upstream {dataset_url.replace('https://', 'https://huggingface.co/datasets/')}.git || git remote set-url upstream {dataset_url.replace('https://', 'https://huggingface.co/datasets/')}.git", cwd=dataset_dir)
    
    # Show remotes
    print("Current remotes:")
    run_command("git remote -v", cwd=dataset_dir)
    
    print(f"\nDataset cloned successfully to {dataset_dir}")
    print("Upstream remote added for future updates")
    
    # Instructions for user
    print("\nTo update from upstream in the future, run:")
    print(f"cd {dataset_dir}")
    print("git fetch upstream")
    print("git merge upstream/main -X theirs")

if __name__ == "__main__":
    main()