# GitHub Secrets Required for Hugging Face Data Sync

To run the GitHub Actions workflow for syncing data from Hugging Face, you need to configure the following secrets in your GitHub repository:

## Required Secrets

1. **HF_TOKEN** (Required)
   - Description: Your Hugging Face access token with write permissions
   - How to obtain:
     - Go to https://huggingface.co/settings/tokens
     - Click "New token"
     - Give it a name (e.g., "github-actions-token")
     - Select "Write" role (or "Admin" if you need full access)
     - Click "Generate"
     - Copy the generated token
   - In your GitHub repo:
     - Go to Settings → Secrets and variables → Actions
     - Click "New repository secret"
     - Name: `HF_TOKEN`
     - Secret: Paste the token you copied

## Optional Secrets

2. **HF_USERNAME** (Optional)
   - Description: Your Hugging Face username
   - Default: 'your-username' (placeholder)
   - How to obtain:
     - This is your username on Hugging Face (the part before `/datasets` in your dataset URL)
     - Example: If your dataset is `https://huggingface.co/datasets/john_doe/my-dataset`, your username is `john_doe`

3. **TARGET_HF_REPO** (Optional)
   - Description: Full URL path to your target Hugging Face dataset repository
   - Default: 'huggingface.co/datasets/your-username/yahoo-finance-data'
   - How to obtain:
     - This is the URL of your Hugging Face dataset repository
     - Format: `huggingface.co/datasets/USERNAME/DATASET_NAME`

## Setting up the Secrets

1. Navigate to your GitHub repository
2. Click on the "Settings" tab
3. In the left sidebar, click on "Secrets and variables"
4. Click on "Actions"
5. Click "New repository secret" for each required secret
6. Enter the name and value for each secret as described above

## Important Notes

- Keep your tokens secure and never share them publicly
- The HF_TOKEN should have write permissions to allow pushing updates to your Hugging Face dataset
- If you don't set the optional secrets, the workflow will use default values that you'll need to update later