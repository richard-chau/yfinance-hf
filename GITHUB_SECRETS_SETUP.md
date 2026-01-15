# GitHub Secrets Setup

To use this repository with the automated sync workflow, you need to configure the following GitHub Secrets:

## Required Secrets

### `HF_TOKEN`
- **Purpose**: Authentication token for Hugging Face API access
- **How to get it**:
  1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
  2. Click on "Access Tokens" tab
  3. Click "New token" button
  4. Give your token a name (e.g., "github-actions-token")
  5. Select the appropriate role (typically "Write" for pushing datasets)
  6. Copy the generated token
- **How to add to GitHub**:
  1. Go to your GitHub repository
  2. Click on "Settings" tab
  3. In the left sidebar, click on "Secrets and variables" → "Actions"
  4. Click "New repository secret"
  5. Name it `HF_TOKEN`
  6. Paste your Hugging Face token as the value
  7. Click "Add secret"

## Important Notes

1. **Security**: Never commit tokens directly to the codebase. Always use GitHub Secrets for sensitive information.

2. **Token Permissions**: The token should have write permissions if you plan to push data to your Hugging Face datasets.

3. **Local Development**: For local development, store your token in the `.env` file in the parent directory (`../.env`) with the format:
   ```
   HF_TOKEN=your_actual_token_here
   ```

4. **Workflow Schedule**: The workflow runs daily at midnight UTC (which is around 8 AM Beijing time).

## Troubleshooting

- If the workflow fails, check the GitHub Actions logs for error messages
- Ensure your Hugging Face token has the correct permissions
- Verify that your target dataset exists on Hugging Face