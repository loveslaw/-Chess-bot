#!/bin/bash

# Chess Bot Git Initialization Script
# This script initializes a git repository for the chess bot project

echo "Initializing git repository for Chess Bot..."

# Initialize git repository
git init

# Configure git user
git config user.name "openhands"
git config user.email "openhands@all-hands.dev"

# Add all files to git
git add .

# Create initial commit
git commit -m "Initial commit: Chess.com selfbot for playing at 3200 rating"

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "Creating .gitignore file..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Test coverage
.coverage
htmlcov/

# Distribution
dist/
build/
*.egg-info/

# Temporary files
*.tmp
*.temp

# Personal files
*.key
*.pem
*.env

# System files
pagefile.sys
hiberfil.sys
swapfile.sys

# Application data
*.sqlite
*.db

# Build directories
build/
dist/

# IDE specific
.vscode/
.idea/

# Python virtual environments
venv/
.env

# System temporary files
/tmp/
*.tmp

# Project specific
*.log
*.pyc
__pycache__/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Test coverage
.coverage
htmlcov/

# Distribution
*.egg-info/

# Temporary files
*.tmp
*.temp

# Personal files
*.key
*.pem
*.env

# System files
pagefile.sys
hiberfil.sys
swapfile.sys

# Application data
*.sqlite
*.db

# Build directories
build/
dist/

# IDE specific
.vscode/
.idea/

# Python virtual environments
venv/
.env

# System temporary files
/tmp/
*.tmp
EOF
    git add .gitignore
    git commit -m "Add .gitignore file"
fi

echo ""
echo "✅ Git repository initialized successfully!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub:"
echo "   git remote add origin <your-github-repo-url>"
echo "   git push -u origin master"
echo ""
echo "2. The project is ready to use:"
echo "   pip install -r requirements.txt"
echo "   python example.py"
