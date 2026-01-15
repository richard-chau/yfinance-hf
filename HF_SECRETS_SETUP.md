# Using the Hugging Face Sync Script

## Prerequisites

Before running the sync script, you need to set up your Hugging Face token:

1. Get your Hugging Face token from [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Update the `../.env` file in the parent directory with your actual token:
   ```
   HF_TOKEN=your_actual_token_here
   ```
   Replace `your_actual_token_here` with your real Hugging Face token.

## Creating Your Target Dataset on Hugging Face

Before the sync workflow can run successfully, you must create your own Hugging Face dataset:

1. Go to https://huggingface.co/new-dataset
2. Create a new dataset with the name "yahoo-finance-data" (or update the workflow file to match your dataset name)
3. Make sure your account has write permissions to this dataset

## Running the Script

To run the sync script locally:

```bash
python sync_hf_data.py
```

## Environment Configuration

The script looks for the HF_TOKEN in the `../.env` file (one directory up from the script location). Make sure this file exists and contains your valid token before running the script.

## GitHub Actions

For the GitHub Actions workflow to work, you need to add the same token as a GitHub Secret named `HF_TOKEN` in your repository settings.