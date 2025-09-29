#!/bin/bash

# Setup script for Job Search Tool
# This script installs uv and sets up the Python dependencies

echo "🚀 Setting up Job Search Tool"
echo "=================================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"

    # Check if installation was successful
    if ! command -v uv &> /dev/null; then
        echo "❌ Failed to install uv. Please install manually:"
        echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
        echo "   Then restart your terminal and run this script again."
        exit 1
    fi

    echo "✅ uv installed successfully!"
else
    echo "✅ uv is already installed"
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    uv venv
    echo "✅ Virtual environment created!"
else
    echo "✅ Virtual environment already exists"
fi

# Install Python dependencies in the virtual environment
echo "📚 Installing Python dependencies..."
uv pip install requests beautifulsoup4 lxml

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies with uv."
    echo "💡 Trying alternative installation methods..."

    # Try with --system flag
    echo "📚 Trying system installation..."
    uv pip install --system requests beautifulsoup4 lxml

    if [ $? -ne 0 ]; then
        # Try with python3 -m pip
        echo "📚 Trying with python3 -m pip..."
        python3 -m pip install requests beautifulsoup4 lxml

        if [ $? -ne 0 ]; then
            echo "❌ All installation methods failed."
            echo "💡 Please try manually:"
            echo "   python3 -m pip install requests beautifulsoup4 lxml"
            echo "   or"
            echo "   pip3 install requests beautifulsoup4 lxml"
        fi
    fi
fi

# Make job_search.py executable
chmod +x job_search.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the job search tool:"
echo "  source .venv/bin/activate  # Activate virtual environment"
echo "  ./job_search.py            # Run the tool"
echo ""
echo "Or run directly with uv:"
echo "  uv run python job_search.py"
echo ""
echo "For help and examples, see:"
echo "  cat README.md"