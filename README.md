# Yahoo Finance Data Mirror

This repository contains a mirror of the [bwzheng2010/yahoo-finance-data](https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data) Hugging Face dataset, automatically synced daily.

## Setup Instructions

### Prerequisites

1. A GitHub account
2. A Hugging Face account (to get an API token if needed)

### Required GitHub Secrets

For the daily sync to work properly, you need to configure the following GitHub Secrets in your repository settings:

#### 1. `HF_TOKEN` (Optional but Recommended)
- **Purpose**: Hugging Face API token for accessing datasets that may have access restrictions
- **How to obtain**:
  1. Go to your [Hugging Face account settings](https://huggingface.co/settings/tokens)
  2. Click on "Access Tokens" tab
  3. Click "New token" button
  4. Give it a name (e.g., "github-sync-token") and select "Read" role
  5. Copy the generated token
  6. In your GitHub repository, go to Settings → Secrets and variables → Actions
  7. Click "New repository secret", name it `HF_TOKEN`, and paste the token value

#### 2. `GITHUB_TOKEN` (Already Available)
- **Purpose**: GitHub automatically provides this token for authenticating with the repository
- **Note**: This is automatically available in GitHub Actions and typically doesn't need to be manually configured

### Setting Up the Daily Sync

The repository is configured with a GitHub Action that runs daily at 00:00 UTC to sync the latest data from the upstream Hugging Face dataset.

## Manual Sync

If you want to manually trigger a sync:
1. Go to the "Actions" tab in your repository
2. Find the "Daily Sync from Hugging Face Dataset" workflow
3. Click "Run workflow" to trigger it manually

## Repository Structure

- `.github/workflows/daily-sync.yml` - GitHub Actions workflow for daily synchronization
- `clone_dataset.py` - Python script to initially clone the dataset with git LFS support

## About Git LFS

This repository uses Git Large File Storage (LFS) to handle large files efficiently. Git LFS replaces large files with text pointers in the repository while storing the file contents on a remote server.

## License

The license for this data follows that of the original [bwzheng2010/yahoo-finance-data](https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data) dataset.