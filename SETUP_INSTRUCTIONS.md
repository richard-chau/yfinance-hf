# Setup Instructions

## GitHub Secrets Required

You need to add the following secrets to your GitHub repository:

### 1. HF_TOKEN
- **Purpose**: Authentication token for Hugging Face
- **How to get it**:
  1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
  2. Click on "New token"
  3. Give it a name (e.g., "github-action-token")
  4. Select "Write" permissions (needed to push updates to your dataset)
  5. Copy the generated token
- **How to add to GitHub**:
  1. Go to your GitHub repository
  2. Navigate to Settings → Secrets and variables → Actions
  3. Click "New repository secret"
  4. Name: `HF_TOKEN`
  5. Paste your Hugging Face token as the value

## Environment Variables

The scripts also look for an `.env` file in the parent directory (`../.env`) with the following format:

```env
HF_TOKEN=your_actual_token_here
```

## Usage

After setting up the secrets:

1. The GitHub Action will automatically run daily to sync the dataset
2. You can also trigger it manually using the "workflow_dispatch" option in the Actions tab

## Important Notes

- The workflow runs at 00:00 UTC (which is 8:00 AM Beijing time)
- The workflow uses `-X theirs` merge strategy to prioritize upstream changes
- The `[skip ci]` tag in the commit message prevents triggering other CI workflows unnecessarily