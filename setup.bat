@echo off
setlocal enabledelayedexpansion

:: 🎧 Podcastify Setup Script for Windows
:: Tự động setup project và push lên GitHub

echo 🎧 Podcastify Setup Script
echo ==========================
echo.

:: Check if Node.js is installed
echo Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 18+ first.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✅ Node.js detected: !NODE_VERSION!
)

:: Check if Git is installed
echo Checking Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git not found. Please install Git first.
    pause
    exit /b 1
) else (
    echo ✅ Git is installed
)

:: Install dependencies
echo.
echo ℹ️  Installing dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
) else (
    echo ✅ Dependencies installed successfully
)

:: Setup environment file
echo.
if not exist ".env.local" (
    echo ℹ️  Creating .env.local file...
    copy .env.example .env.local >nul
    echo ⚠️  Please edit .env.local with your API keys before running the app
    echo ℹ️  You need:
    echo   - OpenAI API Key (required)
    echo   - Google Cloud TTS credentials (optional)
) else (
    echo ✅ .env.local already exists
)

:: Initialize Git repository
echo.
if not exist ".git" (
    echo ℹ️  Initializing Git repository...
    git init
    git add .
    git commit -m "🎉 Initial commit: Podcastify - PDF to Audio Converter with Pastel UI"
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

:: Get GitHub info
echo.
echo ℹ️  GitHub Repository Setup
echo ========================
echo.
set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter repository name (default: podcastify): "
if "!REPO_NAME!"=="" set REPO_NAME=podcastify

echo.
echo ℹ️  Repository will be created at: https://github.com/!GITHUB_USERNAME!/!REPO_NAME!
set /p CONTINUE="Continue? (y/n): "
if /i not "!CONTINUE!"=="y" (
    echo ⚠️  Setup cancelled by user
    pause
    exit /b 1
)

:: Setup GitHub remote
echo.
echo ℹ️  Setting up GitHub remote...
git remote remove origin >nul 2>&1
git remote add origin "https://github.com/!GITHUB_USERNAME!/!REPO_NAME!.git"
echo ✅ GitHub remote configured

echo.
echo ⚠️  Make sure to create the repository on GitHub first!
echo ℹ️  Visit: https://github.com/new
echo ℹ️  Repository name: !REPO_NAME!
echo ℹ️  Description: 🎧 Modern PDF to Audio Converter with Beautiful Pastel UI
echo.
pause

:: Push to GitHub
echo.
echo ℹ️  Pushing code to GitHub...
git push -u origin main
if %errorlevel% neq 0 (
    echo ❌ Failed to push to GitHub
    echo ℹ️  You may need to:
    echo   1. Create the repository on GitHub first
    echo   2. Setup authentication (SSH key or personal access token)
    echo   3. Run: git push -u origin main
) else (
    echo ✅ Code pushed successfully!
    echo ℹ️  Repository URL: https://github.com/!GITHUB_USERNAME!/!REPO_NAME!
)

:: Create release tag
echo.
echo ℹ️  Creating release tag...
git tag -a v1.0.0 -m "🎉 Release v1.0.0: Initial release with pastel UI"
git push origin v1.0.0
if %errorlevel% neq 0 (
    echo ⚠️  Failed to push tag (repository might not exist yet)
) else (
    echo ✅ Release tag created: v1.0.0
)

:: Show next steps
echo.
echo ✅ Setup Complete! 🎉
echo ==================
echo.
echo ℹ️  Next steps:
echo 1. Edit .env.local with your API keys
echo 2. Test locally: npm run dev
echo 3. Deploy to Vercel: see DEPLOYMENT.md
echo.
echo ℹ️  Useful commands:
echo   npm run dev     - Start development server
echo   npm run build   - Build for production
echo   npm run lint    - Run linter
echo.
echo ℹ️  Documentation:
echo   📖 Getting Started: ./GETTING_STARTED.md
echo   🚀 Deployment: ./DEPLOYMENT.md
echo   📚 Git Setup: ./GIT_SETUP.md
echo.
echo ℹ️  Repository: https://github.com/!GITHUB_USERNAME!/!REPO_NAME!
echo.
pause
