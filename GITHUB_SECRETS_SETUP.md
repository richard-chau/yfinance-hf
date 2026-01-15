# GitHub Secrets Setup

To use the automated Hugging Face data sync workflow, you need to configure the following GitHub Secret:

## Required Secrets

### HF_TOKEN
- **Purpose**: Authentication token for accessing Hugging Face datasets
- **How to obtain**:
  1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
  2. Click on "Access Tokens" tab
  3. Click "New token" button
  4. Give it a name (e.g., "github-actions-sync")
  5. Select "Read" role for reading datasets (or "Write" if you need to push updates)
  6. Click "Generate"
  7. Copy the generated token

- **How to add to GitHub**:
  1. Go to your GitHub repository
  2. Click on "Settings" tab
  3. In the left sidebar, click on "Secrets and variables" > "Actions"
  4. Click "New repository secret"
  5. Name: `HF_TOKEN`
  6. Paste the token value you copied from Hugging Face
  7. Click "Add secret"

## Important Notes
- Keep your token secure and never share it publicly
- The token should have appropriate permissions based on what operations you need
- If you need to rotate the token, generate a new one and update the GitHub secret