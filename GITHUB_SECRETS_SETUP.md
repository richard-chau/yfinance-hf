# GitHub Secrets Setup

To use the automated sync workflow, you need to configure the following GitHub Secrets in your repository:

## Required Secrets

### HF_TOKEN
- **Purpose**: Authentication token for Hugging Face API access
- **Permissions**: Needs write access to push to your Hugging Face dataset repository
- **How to obtain**:
  1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
  2. Click "New token"
  3. Give it a name (e.g., "sync-token")
  4. Select "Write" role to allow pushing updates to your dataset
  5. Copy the generated token
- **How to add to GitHub**:
  1. Go to your GitHub repository
  2. Navigate to Settings → Secrets and variables → Actions
  3. Click "New repository secret"
  4. Name it `HF_TOKEN`
  5. Paste your Hugging Face token as the value
  6. Click "Add secret"

## Important Notes

- Make sure your Hugging Face dataset repository exists before running the workflow
- The workflow will fail if the target Hugging Face dataset doesn't exist
- Your token should have write permissions to push to your Hugging Face datasets
- Keep your token secure and never expose it in code or logs