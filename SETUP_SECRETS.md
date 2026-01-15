# GitHub Secrets Setup Instructions

To use the automated sync workflow, you need to configure the following secrets in your GitHub repository.

## Required Secrets

### 1. HF_TOKEN
- **Purpose**: Authentication token for Hugging Face API access
- **Required Permissions**: Read access to the source dataset

### How to get your Hugging Face Token

1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Click on "New token"
3. Give your token a name (e.g., "github-sync-token")
4. Select the role:
   - For public datasets: "Read" role is sufficient
   - For private datasets: "Write" role may be needed
5. Click "Generate a token"
6. Copy the generated token (it will only be shown once)

### How to add the secret to GitHub

1. Go to your GitHub repository
2. Click on "Settings" tab
3. In the left sidebar, click on "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Name: `HF_TOKEN`
6. Secret: Paste your Hugging Face token
7. Click "Add secret"

## Important Notes

- Never share your tokens publicly
- Tokens can be revoked anytime from your Hugging Face account
- If the sync fails, check that your token has the correct permissions
- For public datasets like `bwzheng2010/yahoo-finance-data`, a "Read" token is sufficient