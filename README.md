# Yahoo Finance Data Sync

This repository contains scripts and GitHub Actions workflows to sync Yahoo Finance data from a Hugging Face dataset.

## Setup Instructions

### Prerequisites

1. Install Git LFS:
   ```bash
   git lfs install
   ```

2. Install GitHub CLI (gh):
   ```bash
   # On Ubuntu/Debian
   sudo apt install gh

   # On macOS
   brew install gh

   # On Windows (using Chocolatey)
   choco install gh
   ```

3. Install Python dependencies:
   ```bash
   pip install python-dotenv
   ```

### Required GitHub Secrets

To use this repository, you need to add the following secrets to your GitHub repository:

1. **HF_TOKEN**: Your Hugging Face access token
   - Go to [Hugging Face Tokens](https://huggingface.co/settings/tokens)
   - Create a new token with read access (or write if you need to push updates)
   - Copy the token value
   - In your GitHub repository, go to Settings → Secrets and variables → Actions
   - Add a new secret named `HF_TOKEN` with the copied value

2. **GITHUB_TOKEN**: This is automatically provided by GitHub Actions (no need to set manually)

3. **PAT** (Personal Access Token, optional but recommended for push permissions):
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate a new token with `repo` scope
   - Copy the token value
   - In your GitHub repository, go to Settings → Secrets and variables → Actions
   - Add a new secret named `PAT` with the copied value
   - If you don't set PAT, the workflow will use GITHUB_TOKEN, but you may need to enable workflow permissions (see below)

### GitHub Actions Permissions

For the workflow to run successfully, you need to ensure that GitHub Actions has permission to write to your repository:

1. Go to your repository Settings → Actions → General
2. Under "Workflow permissions", select "Read and write permissions"
3. Check "Allow GitHub Actions to create and approve pull requests"

Note: If you don't want to create a PAT, you can rely on the GITHUB_TOKEN but must enable the workflow permissions as described above.

### Important: Enable Workflow Permissions

For the daily sync to work properly, you need to specifically enable workflow permissions:

1. Go to your repository Settings → Actions → General
2. In the "Workflow permissions" section, select the radio button for "Read and write permissions"
3. Also check the box "Allow GitHub Actions to create and approve pull requests"
4. Click "Save" to apply the changes

This will allow the `github-actions[bot]` to push changes back to your repository.

### Environment Variables

Create a `.env` file in the parent directory (`../.env`) with your tokens:

```env
HF_TOKEN=your_hugging_face_token_here
```

## Usage

### Manual Sync

To manually sync the dataset using the new script:

```bash
python clone_and_setup.py --dataset bwzheng2010/yahoo-finance-data --target-dir ./data
```

To manually sync the dataset using the original script:

```bash
python clone_dataset.py \
  --dataset-url https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data \
  --repo-dir ./data \
  --upstream-url https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data \
  --github-repo-url https://github.com/your-username/your-repo-name \
  --github-token $GITHUB_TOKEN
```

### Automatic Daily Sync

The GitHub Actions workflow will automatically sync the dataset daily at midnight UTC. You can also manually trigger the sync using the "workflow_dispatch" option in the Actions tab of your repository.

## Architecture

- `clone_and_setup.py`: New script to clone the Hugging Face dataset and set up upstream tracking (uses token from ../.env)
- `clone_dataset.py`: Original script to clone the Hugging Face dataset and set up upstream tracking
- `.github/workflows/daily-sync.yml`: GitHub Actions workflow for automatic daily sync
- The workflow uses a dual-remote approach to sync from the Hugging Face dataset to your GitHub repository
- Git LFS is properly configured to handle large files efficiently