# One-Time Setupne 
# Clone the GitHub repository
git clone https://github.com/sirob511/x-news-aggregator.git
cd x-news-aggregator

# Create and activate Python virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install all required libraries
pip install -r requirements.txt

# Daily Use
# Navigate to the project folder
cd C:\Users\boris\x-news-aggregator

# Allow to run scripts on the system  
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Activate virtual environment
.\venv\Scripts\activate

# Exit Virtual Environment
deactivate


# Git Commands
# Check for file changes
git status

# Add all changes
git add .

# Commit with a message
git commit -m "Your commit message"

# Push to GitHub
git push origin main

python rss_to_tweet.py --dry-run
python rss_to_tweet.py


