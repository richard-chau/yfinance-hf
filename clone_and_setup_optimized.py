import os
import subprocess
import sys
from pathlib import Path

def load_env_vars():
    """Load environment variables from .env file"""
    env_path = Path("../.env")
    if not env_path.exists():
        env_path = Path(".env")  # fallback to local .env
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.replace('"', '').replace("'", "")
    
    return os.getenv('HF_TOKEN')

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result"""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(
        cmd,
        shell=isinstance(cmd, str),
        cwd=cwd,
        capture_output=True,
        text=True
    )
    
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(result.returncode)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
        
    return result

def clone_dataset(dataset_repo_url, target_dir, hf_token):
    """Clone the Hugging Face dataset repository"""
    if os.path.exists(target_dir):
        print(f"Directory {target_dir} already exists. Skipping clone.")
        return
    
    # Use token for authentication during clone
    authenticated_url = dataset_repo_url.replace("https://", f"https://hf_:{hf_token}@")
    
    print(f"Cloning dataset from {dataset_repo_url}")
    run_command([
        "git", "clone", authenticated_url, target_dir
    ])

def setup_git_lfs(repo_path):
    """Initialize Git LFS in the repository"""
    print("Initializing Git LFS...")
    run_command(["git", "lfs", "install"], cwd=repo_path)
    
    # Pull LFS files
    print("Pulling LFS files...")
    run_command(["git", "lfs", "pull"], cwd=repo_path)

def setup_upstream_tracking(repo_path, upstream_url):
    """Set up upstream tracking for the repository"""
    print(f"Setting up upstream tracking for {upstream_url}")
    
    # Add upstream remote
    run_command(["git", "remote", "add", "upstream", upstream_url], cwd=repo_path)
    
    # Verify remotes
    print("Current remotes:")
    run_command(["git", "remote", "-v"], cwd=repo_path)

def main():
    # Load HF token from .env
    hf_token = load_env_vars()
    if not hf_token or hf_token == "your_actual_token_here":
        print("ERROR: HF_TOKEN not found in .env file or still has default value.")
        print("Please set your actual Hugging Face token in the .env file.")
        sys.exit(1)
    
    # Dataset information
    dataset_name = "bwzheng2010/yahoo-finance-data"
    dataset_repo_url = f"https://huggingface.co/datasets/{dataset_name}"
    target_dir = "yahoo-finance-data"
    
    # Clone the dataset
    clone_dataset(dataset_repo_url, target_dir, hf_token)
    
    # Initialize Git LFS
    setup_git_lfs(target_dir)
    
    # Set up upstream tracking
    setup_upstream_tracking(target_dir, dataset_repo_url)
    
    print("\nDataset cloned successfully!")
    print(f"Repository located at: {os.path.abspath(target_dir)}")
    print("Upstream remote added as 'upstream'")
    print("\nTo update from upstream later, run:")
    print(f"  cd {target_dir}")
    print("  git fetch upstream")
    print("  git merge upstream/main -X theirs")

if __name__ == "__main__":
    main()