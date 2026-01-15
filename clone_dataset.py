#!/usr/bin/env python3
"""
Script to clone a Hugging Face dataset, set up upstream tracking,
and configure Git LFS for handling large files.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def load_env_vars():
    """Load environment variables from ../.env file or environment variable."""
    # First check if HF_TOKEN is already set as an environment variable
    hf_token = os.getenv('HF_TOKEN')
    if hf_token:
        return hf_token

    env_path = Path(__file__).parent / ".." / ".env"

    # Also check in the parent directory of the parent
    alt_env_path = Path(__file__).parent / "../.." / ".env"

    if env_path.exists():
        env_file = env_path
    elif alt_env_path.exists():
        env_file = alt_env_path
    else:
        print(f"Warning: .env file not found at {env_path} or {alt_env_path}")
        return None

    # Read the .env file manually
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
    return os.getenv('HF_TOKEN')


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and handle errors."""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(
            cmd if isinstance(cmd, list) else cmd.split(),
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error output: {e.stderr}")
        if check:
            raise
        return e


def clone_hf_dataset(dataset_url, repo_dir, hf_token=None):
    """Clone the Hugging Face dataset."""
    print(f"Cloning dataset from {dataset_url} to {repo_dir}")

    # Prepare the clone URL with token if available
    if hf_token:
        # Format for Hugging Face: https://hf_xxx@huggingface.co/...
        clone_url = dataset_url.replace("https://", f"https://hf_{hf_token}@")
    else:
        clone_url = dataset_url

    # Clone the repository
    cmd = ["git", "clone", clone_url, repo_dir]
    run_command(cmd)

    # Initialize and pull LFS files
    print("Initializing Git LFS...")
    run_command(["git", "lfs", "install"], cwd=repo_dir)
    run_command(["git", "lfs", "pull"], cwd=repo_dir)


def setup_upstream_tracking(repo_dir, upstream_url, hf_token=None):
    """Set up upstream tracking for the cloned repository."""
    print(f"Setting up upstream tracking from {upstream_url}")

    # Add upstream remote
    if hf_token:
        # Format for Hugging Face: https://hf_xxx@huggingface.co/...
        upstream_with_token = upstream_url.replace("https://", f"https://hf_{hf_token}@")
    else:
        upstream_with_token = upstream_url

    run_command(["git", "remote", "add", "upstream", upstream_with_token], cwd=repo_dir)

    # Verify remotes
    run_command(["git", "remote", "-v"], cwd=repo_dir)


def setup_direct_push_to_github(repo_dir, github_token, github_repo_url):
    """Configure direct push to GitHub using gh CLI."""
    print(f"Setting up direct push to GitHub: {github_repo_url}")

    # Configure git for GitHub
    run_command(["git", "config", "--local", "user.name", "github-actions[bot]"], cwd=repo_dir)
    run_command(["git", "config", "--local", "user.email", "github-actions[bot]@users.noreply.github.com"], cwd=repo_dir)

    # Check if gh CLI is available
    try:
        run_command(["gh", "--version"])
    except FileNotFoundError:
        print("Error: gh CLI not found. Please install GitHub CLI.")
        return False

    # Authenticate with GitHub if token is provided
    if github_token:
        # Write token to temporary file and authenticate
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tf:
            tf.write(github_token)
            tf.flush()

            run_command(["gh", "auth", "login", "--with-token", "<", tf.name], cwd=repo_dir)
            os.unlink(tf.name)

    return True


def push_to_github(repo_dir, github_token, github_repo_url):
    """Push changes to GitHub repository."""
    print(f"Pushing changes to GitHub: {github_repo_url}")

    # Check if there are changes to commit
    result = run_command(["git", "status", "--porcelain"], cwd=repo_dir, check=False)
    if result.stdout.strip():  # If there are changes
        # Add all changes
        run_command(["git", "add", "."], cwd=repo_dir)

        # Commit changes
        run_command(["git", "commit", "-m", "Sync: Update from upstream [skip ci]"], cwd=repo_dir)

        # Determine the correct way to push based on whether a token is provided
        if github_token:
            # Use the token to push directly
            push_url = github_repo_url.replace("https://", f"https://{github_token}@")
            run_command(["git", "remote", "set-url", "origin", push_url], cwd=repo_dir)

        run_command(["git", "push", "origin", "main"], cwd=repo_dir)

        # If gh CLI is available, also try to push using gh
        try:
            run_command(["gh", "repo", "sync"], cwd=repo_dir)
        except:
            # If gh repo sync fails, that's fine, we've already pushed with git
            pass
    else:
        print("No changes to commit.")


def main():
    parser = argparse.ArgumentParser(description="Clone Hugging Face dataset and set up upstream tracking")
    parser.add_argument("--dataset-url", required=True, help="URL of the Hugging Face dataset")
    parser.add_argument("--repo-dir", required=True, help="Local directory to clone the repo to")
    parser.add_argument("--upstream-url", required=True, help="Upstream URL for tracking")
    parser.add_argument("--github-repo-url", required=True, help="GitHub repository URL for direct push")
    parser.add_argument("--github-token", help="GitHub token for authentication")

    args = parser.parse_args()

    # Load HF token from .env file
    hf_token = load_env_vars()
    if not hf_token:
        print("HF_TOKEN not found in .env file. Proceeding without token (may cause issues with private datasets).")

    # Create the target directory if it doesn't exist
    repo_path = Path(args.repo_dir)
    repo_path.parent.mkdir(parents=True, exist_ok=True)

    # Clone the dataset
    clone_hf_dataset(args.dataset_url, args.repo_dir, hf_token)

    # Set up upstream tracking
    setup_upstream_tracking(args.repo_dir, args.upstream_url, hf_token)

    # Set up direct push to GitHub
    success = setup_direct_push_to_github(args.repo_dir, args.github_token, args.github_repo_url)
    if not success:
        print("Failed to set up direct push to GitHub.")
        sys.exit(1)

    # Push changes to GitHub
    push_to_github(args.repo_dir, args.github_token, args.github_repo_url)

    print(f"Successfully cloned {args.dataset_url} to {args.repo_dir}")
    print("Upstream tracking has been set up.")
    print("Changes have been pushed to GitHub.")


if __name__ == "__main__":
    main()