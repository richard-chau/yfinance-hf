# Install required Python packages
pip install python-dotenv

# Install git-lfs if not already installed
if ! command -v git-lfs &> /dev/null
then
    echo "Installing git-lfs..."
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
    sudo apt-get install git-lfs
fi

# Initialize git-lfs globally
git lfs install