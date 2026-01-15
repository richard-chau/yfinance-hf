# GitHub Secrets Setup

For the Hugging Face data sync workflow to work properly, you need to configure the following GitHub Secret in your repository:

## Required Secrets

### HF_TOKEN
- **Purpose**: Authentication token for Hugging Face API access
- **Value**: Your Hugging Face access token

## How to Get Your Hugging Face Token

1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Click on "Access Tokens" tab
3. Click "New Token" button
4. Give your token a name (e.g., "github-actions-sync")
5. Select the role - choose "Write" or "Admin" depending on your needs
6. Click "Generate"
7. Copy the generated token (you won't be able to see it again)

## How to Add the Secret to GitHub

1. Go to your GitHub repository
2. Click on "Settings" tab
3. In the left sidebar, click on "Secrets and variables" -> "Actions"
4. Click "New repository secret"
5. Name the secret: `HF_TOKEN`
6. Paste your Hugging Face token as the value
7. Click "Add secret"

## Important Notes

- Keep your tokens secure and never share them publicly
- The token in your local `.env` file should match the one you add to GitHub Secrets
- If you regenerate your Hugging Face token, remember to update it in GitHub Secrets as well
- Before running the sync workflow, you must create your own Hugging Face dataset repository at https://huggingface.co/new-dataset
- The dataset name should match what's in the workflow file (e.g., "yahoo-finance-data")
- Make sure your HF token has write permissions to create/push to datasets