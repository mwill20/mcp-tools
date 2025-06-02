# Deploying to Hugging Face Spaces

This guide will help you deploy your MCP Tools application to Hugging Face Spaces.

## Prerequisites

1. A GitHub account
2. A Hugging Face account
3. Git installed on your computer

## Step 1: Push your code to GitHub

If you haven't already created a GitHub repository for this project, follow these steps:

1. Go to [GitHub](https://github.com) and create a new repository
2. Initialize your local repository and push your code:

```bash
# Navigate to your project directory
cd C:\Users\HP\CascadeProjects\MCP_Project

# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit of MCP Tools application"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## Step 2: Create a Hugging Face Space linked to your GitHub repository

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click on "Create new Space"
3. Choose a name for your Space (e.g., "mcp-tools-demo")
4. Select "Gradio" as the SDK
5. Choose "From GitHub repository" as the source
6. Enter your GitHub repository URL
7. Click "Create Space"

## Step 3: Configure your Space

Your Space will automatically use the configuration from your README.md file (the YAML frontmatter at the top).

If you need to make changes to your Space configuration:

1. Go to your Space on Hugging Face
2. Click on the "Settings" tab
3. Update the configuration as needed
4. Click "Save"

## Step 4: Verify your deployment

1. Wait for the build to complete (this may take a few minutes)
2. Once the build is complete, your Space will be available at: https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
3. Test all three tools to make sure they're working correctly

## Troubleshooting

If you encounter any issues with your deployment:

1. Check the build logs on your Hugging Face Space
2. Make sure your dependencies are correctly specified in requirements.txt
3. Verify that your app.py file is correctly configured for deployment
4. Check that your README.md file has the correct configuration in the YAML frontmatter
