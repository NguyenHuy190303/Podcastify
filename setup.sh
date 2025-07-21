#!/bin/bash

# 🎧 Podcastify Setup Script
# Tự động setup project và push lên GitHub

echo "🎧 Podcastify Setup Script"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Node.js is installed
check_node() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_status "Node.js detected: $NODE_VERSION"
    else
        print_error "Node.js not found. Please install Node.js 18+ first."
        exit 1
    fi
}

# Check if Git is installed
check_git() {
    if command -v git &> /dev/null; then
        print_status "Git is installed"
    else
        print_error "Git not found. Please install Git first."
        exit 1
    fi
}

# Install dependencies
install_deps() {
    print_info "Installing dependencies..."
    if npm install; then
        print_status "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        exit 1
    fi
}

# Setup environment file
setup_env() {
    if [ ! -f ".env.local" ]; then
        print_info "Creating .env.local file..."
        cp .env.example .env.local
        print_warning "Please edit .env.local with your API keys before running the app"
        print_info "You need:"
        echo "  - OpenAI API Key (required)"
        echo "  - Google Cloud TTS credentials (optional)"
    else
        print_status ".env.local already exists"
    fi
}

# Initialize Git repository
init_git() {
    if [ ! -d ".git" ]; then
        print_info "Initializing Git repository..."
        git init
        git add .
        git commit -m "🎉 Initial commit: Podcastify - PDF to Audio Converter with Pastel UI"
        print_status "Git repository initialized"
    else
        print_status "Git repository already exists"
    fi
}

# Get GitHub username
get_github_info() {
    echo ""
    print_info "GitHub Repository Setup"
    echo "========================"
    
    read -p "Enter your GitHub username: " GITHUB_USERNAME
    read -p "Enter repository name (default: podcastify): " REPO_NAME
    REPO_NAME=${REPO_NAME:-podcastify}
    
    echo ""
    print_info "Repository will be created at: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    read -p "Continue? (y/n): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Setup cancelled by user"
        exit 1
    fi
}

# Setup GitHub remote
setup_github() {
    print_info "Setting up GitHub remote..."
    
    # Remove existing origin if exists
    git remote remove origin 2>/dev/null || true
    
    # Add new origin
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    
    print_status "GitHub remote configured"
    print_warning "Make sure to create the repository on GitHub first!"
    print_info "Visit: https://github.com/new"
    print_info "Repository name: $REPO_NAME"
    print_info "Description: 🎧 Modern PDF to Audio Converter with Beautiful Pastel UI"
    
    echo ""
    read -p "Press Enter after creating the GitHub repository..."
}

# Push to GitHub
push_to_github() {
    print_info "Pushing code to GitHub..."
    
    if git push -u origin main; then
        print_status "Code pushed successfully!"
        print_info "Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    else
        print_error "Failed to push to GitHub"
        print_info "You may need to:"
        echo "  1. Create the repository on GitHub first"
        echo "  2. Setup authentication (SSH key or personal access token)"
        echo "  3. Run: git push -u origin main"
    fi
}

# Create release tag
create_tag() {
    print_info "Creating release tag..."
    git tag -a v1.0.0 -m "🎉 Release v1.0.0: Initial release with pastel UI"
    
    if git push origin v1.0.0; then
        print_status "Release tag created: v1.0.0"
    else
        print_warning "Failed to push tag (repository might not exist yet)"
    fi
}

# Show next steps
show_next_steps() {
    echo ""
    print_status "Setup Complete! 🎉"
    echo "=================="
    echo ""
    print_info "Next steps:"
    echo "1. Edit .env.local with your API keys"
    echo "2. Test locally: npm run dev"
    echo "3. Deploy to Vercel: see DEPLOYMENT.md"
    echo ""
    print_info "Useful commands:"
    echo "  npm run dev     - Start development server"
    echo "  npm run build   - Build for production"
    echo "  npm run lint    - Run linter"
    echo ""
    print_info "Documentation:"
    echo "  📖 Getting Started: ./GETTING_STARTED.md"
    echo "  🚀 Deployment: ./DEPLOYMENT.md"
    echo "  📚 Git Setup: ./GIT_SETUP.md"
    echo ""
    print_info "Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
}

# Main execution
main() {
    echo ""
    print_info "Starting Podcastify setup..."
    echo ""
    
    # Pre-checks
    check_node
    check_git
    
    # Setup steps
    install_deps
    setup_env
    init_git
    
    # GitHub setup
    get_github_info
    setup_github
    push_to_github
    create_tag
    
    # Completion
    show_next_steps
}

# Run main function
main
