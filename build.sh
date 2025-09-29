#!/bin/bash

# Resume Build Script
# Compiles LaTeX resume and organizes output files
# Usage: ./build.sh --title "senior data scientist" --path sample_new

set -e  # Exit on any error

# Default values
RESUME_TITLE=""
RESUME_PATH=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --title)
            RESUME_TITLE="$2"
            shift 2
            ;;
        --path)
            RESUME_PATH="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 --title <resume_title> --path <resume_path>"
            echo "Example: $0 --title \"senior data scientist\" --path sample_new"
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
if [[ -z "$RESUME_TITLE" ]] || [[ -z "$RESUME_PATH" ]]; then
    echo "❌ Error: Both --title and --path parameters are required"
    echo "Usage: $0 --title <resume_title> --path <resume_path>"
    echo "Example: $0 --title \"senior data scientist\" --path sample_new"
    exit 1
fi

# Construct full path
FULL_PATH="resumes/$RESUME_TITLE/$RESUME_PATH"

# Validate path exists
if [[ ! -d "$SCRIPT_DIR/$FULL_PATH" ]]; then
    echo "❌ Error: Path '$FULL_PATH' does not exist"
    exit 1
fi

# Validate resume.tex exists in the path
if [[ ! -f "$SCRIPT_DIR/$FULL_PATH/resume.tex" ]]; then
    echo "❌ Error: resume.tex not found in '$FULL_PATH'"
    exit 1
fi

echo "🔨 Building LaTeX Resume from: $FULL_PATH"

# Create output directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/output"

# Get the resume variant name (title and path combined)
VARIANT_NAME="${RESUME_TITLE}-${RESUME_PATH}"
OUTPUT_NAME="resume-${VARIANT_NAME}.pdf"

# Clean previous build artifacts for this variant
echo "🧹 Cleaning previous build artifacts..."
rm -rf "$SCRIPT_DIR/build/${VARIANT_NAME}"
mkdir -p "$SCRIPT_DIR/build/${VARIANT_NAME}"
rm -f "$SCRIPT_DIR/output/$OUTPUT_NAME"

# Change to the resume directory
cd "$SCRIPT_DIR/$FULL_PATH"

# Compile LaTeX document
echo "📄 Compiling LaTeX document..."
pdflatex -interaction=nonstopmode resume.tex

# Run twice to ensure references are resolved
echo "🔄 Running second pass for references..."
pdflatex -interaction=nonstopmode resume.tex

# Move build artifacts to variant-specific build folder
echo "📦 Moving build artifacts..."
mv resume.aux resume.fdb_latexmk resume.fls resume.log resume.out resume.synctex.gz "$SCRIPT_DIR/build/${VARIANT_NAME}/" 2>/dev/null || true

# Keep final PDF in the resume directory
echo "📋 Keeping final PDF in resume directory..."
# PDF is already in the correct location (resumes/default/resume.pdf)

# Return to script directory
cd "$SCRIPT_DIR"

echo "✅ Build completed successfully!"
echo "📄 Resume PDF available at: $FULL_PATH/resume.pdf"
echo "🔧 Build artifacts stored in: build/$VARIANT_NAME/"