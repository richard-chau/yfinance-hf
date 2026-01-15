# GitHub Secrets Setup

To run the automated sync from Hugging Face to your repository, you need to configure the following GitHub secrets:

## Required Secrets

### 1. HF_TOKEN
- **Purpose**: Authentication token for Hugging Face API access
- **Permissions needed**: Read access to the source dataset and write access to your target dataset

## How to Obtain HF_TOKEN

1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Click on "New token" 
3. Give your token a name (e.g., "sync-token")
4. Select the appropriate role:
   - For reading datasets: "read" role is sufficient
   - For writing to your own datasets: "write" role is needed
5. Click "Generate a token"
6. Copy the generated token (it will only be shown once)

## Setting up GitHub Secrets

1. Go to your GitHub repository
2. Navigate to "Settings" tab
3. Click on "Secrets and variables" in the left sidebar
4. Click on "Actions" 
5. Click "New repository secret"
6. Add the following secrets:

| Name | Secret |
|------|--------|
| HF_TOKEN | [Your copied token from Hugging Face] |

## Important Notes

- Never share your tokens publicly
- Tokens can be revoked anytime from Hugging Face settings
- If you update your token, remember to update it in GitHub Secrets as well
- The GitHub Action will use this token to authenticate with Hugging Face for both reading the source dataset and writing to your target dataset