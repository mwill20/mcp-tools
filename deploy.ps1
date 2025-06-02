# PowerShell script to help deploy to Hugging Face Spaces
# Run this script in PowerShell to prepare your repository for deployment

Write-Host "MCP Tools Deployment Helper" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git before continuing." -ForegroundColor Red
    exit 1
}

# Check if the directory is a git repository
if (-not (Test-Path -Path ".git")) {
    Write-Host "This directory is not a git repository. Would you like to initialize it? (y/n)" -ForegroundColor Yellow
    $initGit = Read-Host
    if ($initGit -eq "y") {
        git init
        Write-Host "✅ Git repository initialized" -ForegroundColor Green
    } else {
        Write-Host "Skipping git initialization. You'll need to do this manually." -ForegroundColor Yellow
    }
}

# Check for uncommitted changes
$status = git status --porcelain
if ($status) {
    Write-Host "You have uncommitted changes:" -ForegroundColor Yellow
    git status
    
    Write-Host "Would you like to commit these changes? (y/n)" -ForegroundColor Yellow
    $commitChanges = Read-Host
    if ($commitChanges -eq "y") {
        Write-Host "Enter a commit message:" -ForegroundColor Cyan
        $commitMessage = Read-Host
        
        git add .
        git commit -m $commitMessage
        Write-Host "✅ Changes committed" -ForegroundColor Green
    } else {
        Write-Host "Skipping commit. You'll need to commit your changes manually." -ForegroundColor Yellow
    }
}

# Check if remote is set up
$remotes = git remote
if (-not $remotes) {
    Write-Host "No git remote is set up. Would you like to add a GitHub remote? (y/n)" -ForegroundColor Yellow
    $addRemote = Read-Host
    if ($addRemote -eq "y") {
        Write-Host "Enter your GitHub username:" -ForegroundColor Cyan
        $username = Read-Host
        
        Write-Host "Enter your repository name:" -ForegroundColor Cyan
        $repoName = Read-Host
        
        git remote add origin "https://github.com/$username/$repoName.git"
        Write-Host "✅ Remote added: origin -> https://github.com/$username/$repoName.git" -ForegroundColor Green
    } else {
        Write-Host "Skipping remote setup. You'll need to do this manually." -ForegroundColor Yellow
    }
}

# Push to GitHub
Write-Host "Would you like to push your changes to GitHub? (y/n)" -ForegroundColor Yellow
$pushChanges = Read-Host
if ($pushChanges -eq "y") {
    $branch = git branch --show-current
    if (-not $branch) {
        $branch = "main"
    }
    
    Write-Host "Pushing to $branch branch..." -ForegroundColor Cyan
    git push -u origin $branch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Changes pushed to GitHub" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to push changes. Please check the error message above." -ForegroundColor Red
    }
} else {
    Write-Host "Skipping push. You'll need to push your changes manually." -ForegroundColor Yellow
}

# Instructions for Hugging Face Spaces
Write-Host ""
Write-Host "Next Steps for Hugging Face Spaces Deployment:" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "1. Go to https://huggingface.co/spaces" -ForegroundColor White
Write-Host "2. Click on 'Create new Space'" -ForegroundColor White
Write-Host "3. Choose a name for your Space (e.g., 'mcp-tools-demo')" -ForegroundColor White
Write-Host "4. Select 'Gradio' as the SDK" -ForegroundColor White
Write-Host "5. Choose 'From GitHub repository' as the source" -ForegroundColor White
Write-Host "6. Enter your GitHub repository URL" -ForegroundColor White
Write-Host "7. Click 'Create Space'" -ForegroundColor White
Write-Host ""
Write-Host "For more detailed instructions, see the deploy_to_hf.md file." -ForegroundColor White

Write-Host ""
Write-Host "Deployment preparation complete!" -ForegroundColor Green
