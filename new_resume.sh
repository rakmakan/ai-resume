#!/bin/bash

# New Resume Script
# Creates a new resume variant by copying the default template
# Usage: ./new_resume.sh --title "senior data scientist" --name sample_new

set -e  # Exit on any error

# Default values
RESUME_TITLE=""
RESUME_NAME=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_PATH="$SCRIPT_DIR/resumes/default"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --title)
            RESUME_TITLE="$2"
            shift 2
            ;;
        --name)
            RESUME_NAME="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 --title <resume_title> --name <resume_name>"
            echo "Example: $0 --title \"senior data scientist\" --name sample_new"
            echo ""
            echo "This script creates a new resume variant by copying the default template."
            echo "The new resume will be created at: resumes/<resume_title>/<resume_name>/"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$RESUME_TITLE" ]] || [[ -z "$RESUME_NAME" ]]; then
    echo "❌ Error: Both --title and --name parameters are required"
    echo "Usage: $0 --title <resume_title> --name <resume_name>"
    echo "Example: $0 --title \"senior data scientist\" --name sample_new"
    exit 1
fi

# Validate resume name (no spaces, special characters)
if [[ ! "$RESUME_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "❌ Error: Resume name can only contain letters, numbers, underscores, and hyphens"
    echo "Invalid name: '$RESUME_NAME'"
    exit 1
fi

# Check if default template exists
if [[ ! -d "$DEFAULT_PATH" ]]; then
    echo "❌ Error: Default template not found at '$DEFAULT_PATH'"
    echo "Please ensure the default resume template exists before creating new variants."
    exit 1
fi

# Check if target directory already exists
NEW_PATH="$SCRIPT_DIR/resumes/$RESUME_TITLE/$RESUME_NAME"
if [[ -d "$NEW_PATH" ]]; then
    echo "❌ Error: Resume '$RESUME_NAME' already exists at '$NEW_PATH'"
    echo "Please choose a different name or remove the existing resume first."
    exit 1
fi

echo "📝 Creating new resume: $RESUME_TITLE/$RESUME_NAME"

# Create title directory if it doesn't exist
TITLE_PATH="$SCRIPT_DIR/resumes/$RESUME_TITLE"
if [[ ! -d "$TITLE_PATH" ]]; then
    echo "📁 Creating title directory: $RESUME_TITLE"
    mkdir -p "$TITLE_PATH"
fi

# Create the new resume directory
echo "📁 Creating directory structure..."
mkdir -p "$NEW_PATH"

# Copy all files and directories from default
echo "📋 Copying template files..."
cp -r "$DEFAULT_PATH/"* "$NEW_PATH/"

# Remove the generated PDF from the copy (if it exists)
if [[ -f "$NEW_PATH/resume.pdf" ]]; then
    echo "🗑️  Removing old PDF from template..."
    rm "$NEW_PATH/resume.pdf"
fi

echo "✅ Successfully created new resume: $RESUME_TITLE/$RESUME_NAME"
echo "📄 Resume location: resumes/$RESUME_TITLE/$RESUME_NAME/"
echo "🔧 Files copied from template:"
echo "   - resume.tex"
echo "   - sections/ (all section files)"
echo ""
echo "🚀 To build your new resume, run:"
echo "   ./build.sh --title \"$RESUME_TITLE\" --path $RESUME_NAME"
echo ""
echo "💡 You can now customize the files in resumes/$RESUME_TITLE/$RESUME_NAME/ for your specific needs."