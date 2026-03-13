#!/bin/bash

# Script to update GitHub repository with our changes
# This script contains all the necessary commands to push our work to GitHub

echo "Network Analysis Package - GitHub Update Script"
echo "=============================================="

# Navigate to the project directory
cd /home/leo520/pynml/network-analysis-package-github-clean

# Configure Git user information
echo "1. Configuring Git user information..."
git config user.email "trernghwhuare@aliyun.com"
git config user.name "Hua Cheng"

# Initialize repository if it doesn't exist
echo "2. Initializing Git repository (if needed)..."
git init

# Add all files
echo "3. Adding all files to Git..."
git add .

# Commit changes
echo "4. Committing changes..."
git commit -m "Update README with results plotting examples and documentation improvements"

# Rename branch to main if needed
echo "5. Setting up main branch..."
git branch -M main

# Add remote repository
echo "6. Adding remote repository..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/trernghwhuare/network-analysis-workflow.git

# Push to GitHub
echo "7. Pushing to GitHub..."
git push -u origin main

echo "GitHub update process completed!"
echo "If you encounter authentication issues, you may need to:"
echo "1. Generate a personal access token on GitHub"
echo "2. Use the token as your password when prompted"
echo "3. Or configure SSH keys for passwordless authentication"