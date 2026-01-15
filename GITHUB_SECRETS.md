# Required GitHub Secrets

To run the automated sync workflow, you need to configure the following secrets in your GitHub repository:

## HF_TOKEN
- **Purpose**: Authentication token for accessing Hugging Face datasets
- **How to get it**: 
  1. Go to https://huggingface.co/settings/tokens
  2. Click "New token"
  3. Give it a name (e.g., "github-actions-token")
  4. Select "Read" role (or "Write" if you need to upload data)
  5. Copy the generated token
- **How to add to GitHub**:
  1. Go to your GitHub repository
  2. Navigate to Settings > Secrets and variables > Actions
  3. Click "New repository secret"
  4. Name: `HF_TOKEN`
  5. Paste your token as the value

## Notes
- Keep your tokens secure and never expose them in code or logs
- The token in your local `.env` file should match the one you add to GitHub Secrets
- If you update the token, remember to update both the `.env` file and the GitHub Secret