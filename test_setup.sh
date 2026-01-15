#!/bin/bash
# Test script to verify the setup

echo "Testing the Hugging Face dataset sync setup..."

# Check if required files exist
if [ ! -f "clone_dataset.py" ]; then
    echo "ERROR: clone_dataset.py not found!"
    exit 1
fi

if [ ! -f ".github/workflows/daily-sync.yml" ]; then
    echo "ERROR: GitHub Actions workflow not found!"
    exit 1
fi

if [ ! -f "README.md" ]; then
    echo "ERROR: README.md not found!"
    exit 1
fi

echo "✓ All required files exist"

# Check if the .env file exists in parent directory
if [ ! -f "../.env" ]; then
    echo "WARNING: ../.env file not found. This is required for the script to work properly."
else
    echo "✓ .env file found in parent directory"
fi

# Check if Python script has correct shebang
if head -1 clone_dataset.py | grep -q "#!/usr/bin/env python3"; then
    echo "✓ Python script has correct shebang"
else
    echo "WARNING: Python script may not have correct shebang"
fi

# Check if GitHub CLI is available
if command -v gh &> /dev/null; then
    echo "✓ GitHub CLI is available"
else
    echo "ERROR: GitHub CLI is not available"
    exit 1
fi

# Check if git-lfs is available
if command -v git-lfs &> /dev/null; then
    echo "✓ Git LFS is available"
else
    echo "ERROR: Git LFS is not available"
    exit 1
fi

echo ""
echo "Setup verification complete!"
echo ""
echo "To run the sync manually, use:"
echo "python clone_dataset.py \\"
echo "  --dataset-url \"https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data\" \\"
echo "  --repo-dir \"./yahoo-finance-data\" \\"
echo "  --upstream-url \"https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data\" \\"
echo "  --github-repo-url \"your_github_repo_url\" \\"
echo "  --github-token \"your_github_token_if_needed\""
echo ""
echo "The GitHub Actions workflow is set to run daily at midnight UTC."
echo "Make sure to add your HF_TOKEN as a GitHub Secret in your repository settings."