#!/usr/bin/env python3
"""
Script to clone a Hugging Face dataset, initialize git lfs,
and set the original dataset as upstream for synchronization.
"""

import os
import sys
import subprocess
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

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get HF token from environment
    hf_token = os.getenv('HF_TOKEN')
    if not hf_token or hf_token == 'your_actual_token_here':
        print("Error: HF_TOKEN not found in .env file or still set to default value.")
        print("Please update the .env file with your actual Hugging Face token.")
        print("Get your token from https://huggingface.co/settings/tokens")
        sys.exit(1)
    
    # Dataset information
    dataset_name = "bwzheng2010/yahoo-finance-data"
    dataset_url = f"https://huggingface.co/datasets/{dataset_name}"
    clone_url = f"https://{hf_token}@huggingface.co/datasets/{dataset_name}"
    
    # Clone the dataset
    print(f"Cloning dataset from: {dataset_url}")
    run_command(['git', 'clone', clone_url])
    
    # Change to the cloned directory
    dataset_dir = dataset_name.split('/')[-1]  # Get the last part of the dataset name
    dataset_path = Path(dataset_dir)
    
    if not dataset_path.exists():
        # If the directory name is different, try to find it
        dirs = [d for d in Path('.').iterdir() if d.is_dir()]
        if len(dirs) == 1:
            dataset_path = dirs[0]
        else:
            print(f"Could not find the cloned dataset directory: {dataset_dir}")
            sys.exit(1)
    
    print(f"Changing to directory: {dataset_path}")
    
    # Initialize git lfs in the cloned repository
    print("Initializing git lfs...")
    run_command(['git', 'lfs', 'install'], cwd=dataset_path)
    
    # Set the original dataset as upstream
    print("Setting original dataset as upstream...")
    run_command(['git', 'remote', 'add', 'upstream', dataset_url], cwd=dataset_path)
    
    # Fetch from upstream
    print("Fetching from upstream...")
    run_command(['git', 'fetch', 'upstream'], cwd=dataset_path)
    
    print(f"\nDataset cloned successfully to '{dataset_path}'")
    print(f"Upstream remote added as 'upstream': {dataset_url}")
    print("You can now synchronize with upstream using:")
    print(f"  cd {dataset_path}")
    print("  git fetch upstream")
    print("  git merge upstream/main")  # or whatever the default branch is
    
    # Show current remotes
    print("\nCurrent remotes:")
    result = run_command(['git', 'remote', '-v'], cwd=dataset_path, check=False)
    print(result.stdout)

if __name__ == "__main__":
    main()