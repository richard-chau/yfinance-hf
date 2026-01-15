# Hugging Face Dataset Sync Setup

This project contains scripts and workflows to automatically sync a Hugging Face dataset from an upstream source.

## Setup Instructions

### 1. Environment Variables

The project expects a `HF_TOKEN` variable in the `../.env` file. Add your Hugging Face token to the `.env` file in the parent directory:

```bash
# In the parent directory (../.env)
HF_TOKEN=your_hugging_face_token_here
```

### 2. GitHub Secrets Required

For the GitHub Actions workflow to work, you need to configure the following secrets in your GitHub repository:

1. `HF_TOKEN`: Your Hugging Face access token with write permissions
2. `GITHUB_ACTOR`: This is automatically provided by GitHub Actions (your GitHub username)

#### How to get your Hugging Face Token:

1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Click on "Access Tokens" in the sidebar
3. Click "New token"
4. Give it a name (e.g., "GitHub Actions Sync")
5. Select "Write" permissions (or "Admin" if you need full access)
6. Click "Generate"
7. Copy the generated token (you won't see it again)

#### How to add the secret to GitHub:

1. Go to your GitHub repository
2. Click on "Settings"
3. In the left sidebar, click on "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Name: `HF_TOKEN`
6. Paste your token in the Value field
7. Click "Add secret"

### 3. Update the Workflow

Before the workflow will work, you need to update the workflow file to use your actual Hugging Face username:

In `.github/workflows/sync-dataset.yml`, change:
- Replace `winterandchaiyun` with your actual Hugging Face username in the target remote URL

### 4. Run the Initial Clone

To initially clone the dataset and set up upstream tracking, run:

```bash
python clone_dataset.py
```

This script will:
- Load your HF token from the .env file
- Clone the dataset from Hugging Face
- Initialize Git LFS
- Set up the upstream remote for future updates

## Usage

The workflow is scheduled to run daily at midnight UTC (8 AM Beijing time). You can also manually trigger it by going to the "Actions" tab in your GitHub repository and running the "Daily Sync to My HF Dataset" workflow.

To manually sync from upstream in the future, navigate to your dataset directory and run:
```bash
git fetch upstream
git merge upstream/main -X theirs
```