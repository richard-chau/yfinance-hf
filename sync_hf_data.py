import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

def load_hf_token():
    """Load HF token from ../.env file"""
    # Load from parent directory as specified
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    
    hf_token = os.getenv('HF_TOKEN')
    if not hf_token or hf_token == 'your_actual_token_here':
        raise ValueError("HF_TOKEN not found in ../.env file or still has default value. Please update the .env file with your actual token.")
    
    return hf_token

def initialize_git_lfs():
    """Initialize git lfs to handle large files"""
    print("Initializing Git LFS...")
    try:
        subprocess.run(['git', 'lfs', 'install'], check=True)
        print("Git LFS initialized successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing Git LFS: {e}")
        sys.exit(1)

def sync_from_upstream(hf_token):
    """Sync data from upstream Hugging Face dataset"""
    print("Starting sync from upstream Hugging Face dataset...")
    
    # Add upstream remote
    upstream_url = "https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data"
    try:
        subprocess.run(['git', 'remote', 'add', 'upstream', upstream_url], check=True)
        print("Added upstream remote successfully.")
    except subprocess.CalledProcessError:
        # Remote might already exist, try removing and re-adding
        try:
            subprocess.run(['git', 'remote', 'remove', 'upstream'], check=True)
            subprocess.run(['git', 'remote', 'add', 'upstream', upstream_url], check=True)
            print("Re-added upstream remote successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error managing upstream remote: {e}")
            sys.exit(1)
    
    # Fetch from upstream
    try:
        subprocess.run(['git', 'fetch', 'upstream', 'main'], check=True)
        print("Fetched upstream data successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error fetching upstream data: {e}")
        sys.exit(1)
    
    # Merge upstream data (using theirs in case of conflicts)
    try:
        subprocess.run(['git', 'merge', 'upstream/main', '-m', 'Auto-sync from bwzheng2010', '-X', 'theirs'], check=True)
        print("Merged upstream data successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error merging upstream data: {e}")
        sys.exit(1)
    
    # Add all files (this will handle LFS files properly)
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print("Added files to git index.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding files to git: {e}")
        sys.exit(1)
    
    # Commit changes
    try:
        subprocess.run(['git', 'commit', '-m', 'Sync latest data from upstream'], check=True)
        print("Committed changes.")
    except subprocess.CalledProcessError:
        # May not need to commit if no changes
        print("No changes to commit or commit already exists.")

def push_to_target_repo(hf_token):
    """Push changes to target Hugging Face dataset"""
    print("Pushing changes to target Hugging Face dataset...")
    
    target_url = f"https://winterandchaiyun:{hf_token}@huggingface.co/datasets/winterandchaiyun/yahoo-finance-data"
    
    try:
        # Add target remote
        subprocess.run(['git', 'remote', 'add', 'target', target_url], check=True)
        print("Added target remote successfully.")
    except subprocess.CalledProcessError:
        # Remote might already exist, try removing and re-adding
        try:
            subprocess.run(['git', 'remote', 'remove', 'target'], check=True)
            subprocess.run(['git', 'remote', 'add', 'target', target_url], check=True)
            print("Re-added target remote successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error managing target remote: {e}")
            sys.exit(1)
    
    # Push to target
    try:
        subprocess.run(['git', 'push', 'target', 'main', '--force'], check=True)
        print("Pushed changes to target Hugging Face dataset successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing to target: {e}")
        sys.exit(1)

def main():
    """Main function to sync data from Hugging Face dataset"""
    print("Starting Hugging Face data sync process...")
    
    # Load HF token
    hf_token = load_hf_token()
    print("Loaded HF token from ../.env file.")
    
    # Initialize Git LFS
    initialize_git_lfs()
    
    # Sync from upstream
    sync_from_upstream(hf_token)
    
    # Push to target repo
    push_to_target_repo(hf_token)
    
    print("Hugging Face data sync completed successfully!")

if __name__ == "__main__":
    main()