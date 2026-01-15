# Hugging Face Dataset Sync

This repository contains scripts and workflows to automatically sync a Hugging Face dataset from an upstream source.

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Hugging Face token in the `.env` file:
   - Get your token from [Hugging Face Settings](https://huggingface.co/settings/tokens)
   - Replace `your_actual_token_here` in `.env` with your actual token

4. Create your own Hugging Face dataset repository (CRITICAL STEP):
   - Go to [Hugging Face Hub](https://huggingface.co/datasets)
   - Click "New Dataset"
   - Choose a name like `your-username/yahoo-finance-data`
   - Make sure to enable Git-based operations
   - NOTE: The GitHub Actions workflow will FAIL until you create this dataset repository

5. Update the GitHub Actions workflow files to use your username:
   - Several workflow files exist in `.github/workflows/`
   - Update all references from `winterandchaiyun` to your actual GitHub/HF username
   - The files have been updated to use `richard-chau` as an example

## GitHub Secrets Required

For the GitHub Actions workflow to work, you need to set up the following secrets in your GitHub repository:

1. `HF_TOKEN`: Your Hugging Face access token with write permissions
   - Go to Settings → Secrets and variables → Actions
   - Add a new secret named `HF_TOKEN`
   - Paste your Hugging Face token as the value

### How to Get Your Hugging Face Token

1. Visit [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Give it a name (e.g., "sync-token")
4. Select "Write" role if you plan to push updates to your dataset
5. Copy the generated token and store it securely

## GitHub Actions Workflow

The workflow in `.github/workflows/sync_hf_data.yml` will:
- Run daily at midnight UTC
- Fetch the latest data from the upstream dataset (bwzheng2010/yahoo-finance-data)
- Merge changes (preferring upstream in case of conflicts)
- Push updates to your repository

You can also manually trigger the workflow from the Actions tab in your GitHub repository.

## Manual Sync

To manually sync the dataset, run:
```bash
python sync_hf_data.py
```

## Notes

- The workflow uses `git lfs` to handle large files properly
- Conflicts are resolved by preferring upstream changes (`-X theirs`)
- The `[skip ci]` tag in commit messages prevents triggering additional CI runs
- Make sure your Hugging Face dataset repository exists before running the workflow