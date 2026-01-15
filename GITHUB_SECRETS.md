# GitHub Secrets Setup

This project requires certain secrets to be configured in your GitHub repository for the automated sync to work properly.

## Required GitHub Secrets

### 1. HF_TOKEN
- **Purpose**: Your Hugging Face access token with write permissions
- **Name**: `HF_TOKEN`
- **Value**: Your actual Hugging Face token

## How to Get Your Hugging Face Token

1. Visit [Hugging Face Settings - Tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Give it a name (e.g., "github-sync-token")
4. Select "Write" role (needed for pushing updates to your dataset)
5. Click "Generate a token"
6. Copy the generated token immediately (it won't be shown again)

## How to Add Secrets to Your GitHub Repository

1. Go to your GitHub repository
2. Click on the "Settings" tab
3. In the left sidebar, click on "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Enter the secret name (e.g., `HF_TOKEN`)
6. Paste the corresponding value
7. Click "Add secret"

## Important Notes

- Keep your tokens secure and never share them publicly
- The GitHub Actions workflow will use these secrets to authenticate with Hugging Face
- Without these secrets properly configured, the sync workflow will fail
- Make sure your Hugging Face dataset repository exists before running the workflow