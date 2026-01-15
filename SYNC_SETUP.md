# Hugging Face Dataset Sync Setup

This project contains scripts and workflows to automatically sync a Hugging Face dataset to your GitHub repository.

## Setup Instructions

### 1. Environment Variables

Make sure you have a `.env` file in the root directory with your Hugging Face token:

```bash
HF_TOKEN=your_hugging_face_token_here
```

### 2. GitHub Secrets Required

You need to add the following secret to your GitHub repository:

- `HF_TOKEN`: Your Hugging Face access token with write permissions

#### How to get your Hugging Face Token:

1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Click on "New token"
3. Give it a name (e.g., "GitHub Sync")
4. Select "Write" permissions (or "Admin" if you need full access)
5. Copy the generated token
6. Go to your GitHub repository
7. Navigate to Settings → Secrets and variables → Actions
8. Click "New repository secret"
9. Name it `HF_TOKEN` and paste your token value

### 3. Running the Script

To clone the dataset locally:

```bash
python clone_dataset.py
```

### 4. GitHub Actions Workflow

The workflow is scheduled to run daily at midnight UTC. You can also trigger it manually from the Actions tab in your GitHub repository.

## Notes

- The workflow uses git-lfs to handle large files properly
- The sync is one-way: from the upstream dataset to your repository
- Conflicts are resolved by taking the upstream version (`-X theirs`)