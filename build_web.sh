#!/bin/bash

# Web Build Script for Lazy Me Today Too
# This script builds the game for web deployment using pygbag

set -e  # Exit on error

echo "🎮 Building Lazy Me Today Too for Web..."
echo "========================================"

# Check if pygbag is installed
if ! command -v pygbag &> /dev/null; then
    echo "❌ pygbag is not installed!"
    echo "Installing pygbag..."
    pip install pygbag
fi

# Clean previous build
if [ -d "build/web" ]; then
    echo "🧹 Cleaning previous web build..."
    rm -rf build/web
fi

# Create output directory
mkdir -p build/web

# Build with pygbag
echo "🔨 Building web version..."
echo "This may take a few minutes on first build..."

# Run pygbag to build the game
# --template can be used to specify custom HTML template
# --app_name sets the application name
# --ume_block sets the size in MB for the filesystem
pygbag --build main.py

echo ""
echo "✅ Build complete!"
echo ""
echo "📁 Output location: build/web"
echo ""
echo "🚀 To test locally:"
echo "   python -m http.server --directory build/web 8000"
echo "   Then open http://localhost:8000 in your browser"
echo ""
echo "📤 To deploy to GitHub Pages:"
echo "   1. Push the 'build/web' folder contents to the 'gh-pages' branch"
echo "   2. Enable GitHub Pages in your repository settings"
echo "   3. Or use the GitHub Actions workflow (.github/workflows/deploy.yml)"
echo ""
