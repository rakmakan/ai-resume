# AI-Powered Resume System

An end-to-end automated system for creating tailored resumes using AI. This system searches for jobs, creates customized resume variants, uses Claude AI to tailor content to job descriptions, and builds professional PDFs.

## 🚀 Quick Start (NEW: Automated Workflow)

```bash
# 1. Install dependencies
poetry install

# 2. List available workflow configurations
python run_workflow.py --list-configs

# 3. Run complete end-to-end workflow
python run_workflow.py --config data_scientist_remote

# That's it! The system will:
# - Search for jobs matching your criteria
# - Let you select which jobs to apply to
# - Use AI to tailor your resume for each job
# - Build professional PDFs automatically
```

📖 **[Full Workflow Documentation →](WORKFLOW.md)**

---

## About This System

This is a powerful resume builder that supports multiple resume variants with modular LaTeX sections. Each resume variant can be customized independently while sharing common build infrastructure.

### Two Ways to Use This System:

1. **🤖 Automated Workflow (Recommended)**: Use the AI-powered workflow for end-to-end automation
   - See [WORKFLOW.md](WORKFLOW.md) for details

2. **🔧 Manual Mode**: Use individual scripts for fine-grained control
   - Continue reading below for manual usage

## File Structure

```
Resume/
├── build.sh              # Build script for compiling resumes
├── new_resume.sh          # Script for creating new resume variants
├── resumes/               # Directory containing resume variants
│   ├── default/           # Default resume template
│   │   ├── resume.tex     # Main LaTeX file
│   │   ├── resume.pdf     # Generated PDF (after building)
│   │   └── sections/      # Modular section files
│   │       ├── header.tex      # Contact information and name
│   │       ├── education.tex   # Education section
│   │       ├── experience.tex  # Work experience section
│   │       ├── projects.tex    # Projects section
│   │       └── skills.tex      # Technical skills section
│   └── [title]/           # Resume title categories
│       └── [variant]/     # Specific resume variants under each title
│           ├── resume.tex     # Main LaTeX file
│           ├── resume.pdf     # Generated PDF (after building)
│           └── sections/      # Modular section files
├── build/                 # Build artifacts (organized by variant)
│   └── [title-variant]/   # LaTeX build files (.aux, .log, etc.)
├── output/                # Legacy output directory
└── README.md              # This file
```

## Quick Start

### Building an Existing Resume
```bash
# Build the default resume
./build.sh --path resumes/default

# Build a titled resume variant
./build.sh --title "senior data scientist" --path sample_new

# Build any other variant
./build.sh --title "software engineer" --path frontend_specialist
```

### Creating a New Resume Variant
```bash
# Create a new resume based on the default template
./new_resume.sh --title "senior data scientist" --name sample_new

# This creates: resumes/senior data scientist/sample_new/
# Then customize the files and build with:
./build.sh --title "senior data scientist" --path sample_new
```

## How It Works

### Resume Structure
Each resume variant contains:
- **`resume.tex`**: Main LaTeX file with document structure and `\input{}` commands
- **`sections/`**: Directory with modular section files
- **`resume.pdf`**: Generated PDF output (created after building)

### Build System
- **`build.sh`**: Compiles LaTeX, manages build artifacts, outputs PDF to source directory
- **`new_resume.sh`**: Creates new resume variants by copying the default template
- **Build artifacts**: Stored in `build/[variant]/` to keep source directories clean

## Script Usage

### build.sh
```bash
# For default template
./build.sh --path resumes/default

# For titled variants
./build.sh --title <resume_title> --path <variant_name>

# Examples:
./build.sh --title "senior data scientist" --path sample_new
./build.sh --title "software engineer" --path frontend_specialist
./build.sh --title "product manager" --path tech_lead

# Help:
./build.sh --help
```

**Features:**
- Compiles LaTeX with two passes for proper references
- Stores build artifacts in organized directories
- Outputs PDF directly in the resume variant directory
- Provides clear success/error messages

### new_resume.sh
```bash
./new_resume.sh --title <resume_title> --name <variant_name>

# Examples:
./new_resume.sh --title "senior data scientist" --name sample_new
./new_resume.sh --title "software engineer" --name frontend_specialist
./new_resume.sh --title "product manager" --name tech_lead

# Help:
./new_resume.sh --help
```

**Features:**
- Copies the default template to create new variants
- Validates resume names (letters, numbers, underscores, hyphens only)
- Prevents overwriting existing variants
- Removes old PDFs from template copies

## Workflow Examples

### Creating Resume for Different Roles
```bash
# Create specialized resumes
./new_resume.sh --title "software engineer" --name frontend_developer
./new_resume.sh --title "software engineer" --name backend_engineer
./new_resume.sh --title "data scientist" --name ml_specialist

# Customize each variant's sections
# Edit resumes/software engineer/frontend_developer/sections/skills.tex (focus on React, CSS, etc.)
# Edit resumes/software engineer/backend_engineer/sections/skills.tex (focus on APIs, databases, etc.)

# Build specific versions
./build.sh --title "software engineer" --path frontend_developer
./build.sh --title "software engineer" --path backend_engineer
./build.sh --title "data scientist" --path ml_specialist
```

### Updating All Variants
```bash
# Update common sections across variants
# Edit resumes/default/sections/experience.tex
# Copy updates to other variants as needed

# Rebuild all variants
./build.sh --path resumes/default
./build.sh --title "software engineer" --path frontend_developer
./build.sh --title "software engineer" --path backend_engineer
./build.sh --title "data scientist" --path ml_specialist
```

## Modifying Sections

To edit any section:
1. Navigate to `resumes/[title]/[variant]/sections/`
2. Edit the desired `.tex` file
3. Rebuild: `./build.sh --title "[title]" --path [variant]`
4. Check the updated PDF: `resumes/[title]/[variant]/resume.pdf`

## Benefits of This System

- **Multi-Variant Support**: Maintain different resume versions for different roles
- **Modular Sections**: Easy to update individual sections without affecting others
- **Clean Organization**: Build artifacts and outputs are properly organized
- **Easy Duplication**: Quickly create new variants based on existing templates
- **Automated Building**: Simple scripts handle complex LaTeX compilation
- **Version Control Friendly**: Clear separation between source, build artifacts, and outputs

## Adding New Sections

1. Create a new `.tex` file in `resumes/[title]/[variant]/sections/`
2. Add the section content using existing LaTeX commands
3. Add `\input{sections/newsection}` to `resume.tex` at the desired position
4. Rebuild with `./build.sh --title "[title]" --path [variant]`

## Troubleshooting

### Build Errors
- Check LaTeX syntax in your `.tex` files
- Ensure all `\input{}` references point to existing files
- Build artifacts and logs are in `build/[title-variant]/` for debugging

### Script Issues
- Use `--help` flag with either script for usage information
- Ensure resume names contain only valid characters
- Check that the default template exists before creating new variants