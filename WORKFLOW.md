# AI Resume Workflow Guide

A comprehensive end-to-end workflow for creating tailored resumes using AI.

## Quick Start

```bash
# 1. Install dependencies
poetry install

# 2. List available configurations
python run_workflow.py --list-configs

# 3. Run a workflow
python run_workflow.py --config data_scientist_remote
```

## Overview

The workflow consists of 4 main steps:

```
┌─────────────────┐
│  1. Job Search  │  Search LinkedIn/job boards for positions
└────────┬────────┘
         │
┌────────▼────────┐
│ 2. Create       │  Create resume folders for each job
│    Folders      │  (copies from default template)
└────────┬────────┘
         │
┌────────▼────────┐
│ 3. AI Tailoring │  Claude AI customizes resume sections
│                 │  based on job description
└────────┬────────┘
         │
┌────────▼────────┐
│ 4. Build PDFs   │  Compile LaTeX to professional PDFs
└─────────────────┘
```

## Configuration File

All workflows are defined in `workflow_config.yaml`. Each configuration specifies:

### Example Configuration

```yaml
configs:
  data_scientist_remote:
    name: "Data Scientist - Remote Positions"
    description: "Search for remote Data Scientist roles"

    # Step 1: Job Search
    job_search:
      enabled: true
      title: "Data Scientist"
      keywords: ["machine learning", "python", "sql"]
      location: "Remote"
      num_results: 20
      filters:
        job_type: ["Full-time"]
        seniority_level: ["Mid-Senior level"]

    # Step 2: Folder Creation
    folder_creation:
      enabled: true
      selection_mode: "manual"  # manual, all, or auto

    # Step 3: AI Tailoring
    ai_tailoring:
      enabled: true
      sections_to_tailor: ["experience", "skills", "projects"]
      process_mode: "sequential"

    # Step 4: Build
    build:
      enabled: true
      compiler: "pdflatex"

    # Workflow Control
    workflow:
      confirmations:
        after_search: true
        after_folder_creation: true
        after_tailoring: true
        after_build: true
      save_state: true
```

## Configuration Options

### Job Search Configuration

| Option | Type | Description | Example |
|--------|------|-------------|---------|
| `enabled` | boolean | Enable this step | `true` |
| `title` | string | Job title to search | `"Data Scientist"` |
| `keywords` | list | Keywords to filter | `["python", "ML"]` |
| `location` | string | Location filter | `"Remote"` |
| `num_results` | int | Max results | `20` |
| `filters.job_type` | list | Job types | `["Full-time"]` |
| `filters.seniority_level` | list | Seniority levels | `["Senior"]` |
| `filters.min_applicants` | int | Min applicants | `0` |
| `filters.max_applicants` | int | Max applicants | `100` |

### Folder Creation Configuration

| Option | Type | Description | Values |
|--------|------|-------------|--------|
| `enabled` | boolean | Enable this step | `true`/`false` |
| `selection_mode` | string | How to select jobs | `"manual"`, `"all"`, `"auto"` |
| `auto_selection.max_applicants` | int | Auto-select if < N applicants | `50` |
| `auto_selection.required_keywords` | list | Must contain keywords | `["python"]` |

**Selection Modes:**
- **manual**: You choose which jobs to process (interactive)
- **all**: Process all found jobs automatically
- **auto**: Auto-select based on criteria (e.g., < 50 applicants)

### AI Tailoring Configuration

| Option | Type | Description | Example |
|--------|------|-------------|---------|
| `enabled` | boolean | Enable AI tailoring | `true` |
| `sections_to_tailor` | list | Which sections to modify | `["experience", "skills"]` |
| `process_mode` | string | Processing mode | `"sequential"` |
| `ai_config.model` | string | Claude model to use | `"claude-sonnet-4-5"` |
| `ai_config.tools` | list | Allowed tools | `["Read", "Edit"]` |

**Process Modes:**
- **sequential**: Process one resume at a time (with progress updates)
- **batch**: Process all at once (faster, less visibility)
- **selective**: Only process specific companies

### Build Configuration

| Option | Type | Description | Example |
|--------|------|-------------|---------|
| `enabled` | boolean | Enable PDF build | `true` |
| `compiler` | string | LaTeX compiler | `"pdflatex"` |
| `runs` | int | Compilation passes | `2` |
| `clean_artifacts` | boolean | Remove .aux files | `true` |
| `build_mode` | string | Build mode | `"all"` |

### Workflow Control

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `confirmations.after_search` | boolean | Confirm after job search | `true` |
| `confirmations.after_folder_creation` | boolean | Confirm after folders | `true` |
| `confirmations.after_tailoring` | boolean | Confirm after AI | `true` |
| `confirmations.after_build` | boolean | Confirm after build | `true` |
| `save_state` | boolean | Save progress | `true` |
| `continue_on_error` | boolean | Continue if error | `false` |
| `state_file` | string | State file path | `".workflow_state.json"` |

### Logging Configuration

| Option | Type | Description | Values |
|--------|------|-------------|--------|
| `level` | string | Log level | `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"` |
| `console` | boolean | Log to console | `true` |
| `file` | string | Log file path | `"logs/workflow_{timestamp}.log"` |

## Usage Examples

### Basic Usage

```bash
# Run complete workflow with confirmations
python run_workflow.py --config data_scientist_remote
```

### List Available Configs

```bash
python run_workflow.py --list-configs
```

Output:
```
📋 Available Configurations:
================================================================================

🔹 data_scientist_remote
   Name: Data Scientist - Remote Positions
   Description: Search for remote Data Scientist roles and create tailored resumes
   Job Title: Data Scientist
   Location: Remote

🔹 ml_engineer_toronto
   Name: ML Engineer - Toronto
   Description: Machine Learning Engineer positions in Toronto area
   Job Title: Machine Learning Engineer
   Location: Toronto, ON, Canada
```

### Resume from Specific Step

If workflow was interrupted:

```bash
# Resume from last saved state
python run_workflow.py --config data_scientist_remote --resume

# Or resume from specific step
python run_workflow.py --config data_scientist_remote --resume-from step3
```

### Custom Config File

```bash
python run_workflow.py --config-file my_custom_config.yaml --config my_config
```

## Workflow Steps in Detail

### Step 1: Job Search

The job search step:
1. Runs `fetch_job/job_search.py` with your parameters
2. Searches LinkedIn/job boards
3. Saves results to `job_search_output/YYYY-MM-DD/job_title_HHMMSS.json`
4. Shows summary (number of jobs found)
5. Asks for confirmation

**What you'll see:**
```
============================================================
📋 STEP 1: JOB SEARCH
============================================================
Job Title: Data Scientist
Location: Remote
Results: 20

🔍 Running job search...
✅ Job search completed: job_search_output/2025-09-29/data_scientist_143022.json

📊 Found 18 jobs

Continue to next step (Folder Creation)? [Y/n]:
```

### Step 2: Folder Creation

The folder creation step:
1. Reads job search results
2. Shows you all found jobs
3. Prompts you to select (if selection_mode="manual"):
   - Enter job number (e.g., `3`)
   - Enter multiple jobs (e.g., `1,3,5`)
   - Enter `all` for all jobs
4. Creates folder structure:
   ```
   resumes/
   └── Data Scientist/
       ├── google_a1b2c3/
       │   ├── job_details.json
       │   ├── resume.tex
       │   └── sections/
       ├── meta_d4e5f6/
       └── ...
   ```
5. Asks for confirmation

**What you'll see:**
```
============================================================
📁 STEP 2: FOLDER CREATION
============================================================
Selection mode: manual
Job search output: job_search_output/2025-09-29/data_scientist_143022.json

📂 Creating resume folders...
(You will be prompted to select jobs)

📋 Available jobs:

1. Senior Data Scientist
   Company: Google
   Location: Remote
   Applicants: 45

2. Data Scientist
   Company: Meta
   Location: Menlo Park, CA
   Applicants: 120

...

🎯 Select job number (1-18), multiple jobs (e.g., 1,2,3), or 'all': 1,5,8

✅ Created 3 resume folders
   - google_a1b2c3
   - microsoft_x9y8z7
   - netflix_p0q1r2

Continue to next step (AI Tailoring)? [Y/n]:
```

### Step 3: AI Tailoring

The AI tailoring step:
1. For each selected resume folder:
2. Reads `job_details.json`
3. Renders prompt with job description
4. Calls Claude AI CLI
5. Claude analyzes job requirements
6. Claude modifies resume sections to match:
   - Reorders experience bullets (most relevant first)
   - Emphasizes matching skills
   - Highlights relevant projects
   - Uses keywords from job description (ATS optimization)
7. Saves modified `.tex` files
8. Asks for confirmation

**What you'll see:**
```
============================================================
🤖 STEP 3: AI RESUME TAILORING
============================================================
Processing 3 resumes in sequential mode

[1/3] Processing: google_a1b2c3
🔄 Running AI tailoring...
🤖 Calling Claude AI to tailor resume sections...
📂 Working directory: resumes/Data Scientist/google_a1b2c3
⚡ Running Claude AI with real-time output...
--------------------------------------------------------------------------------
[Claude's output streams here in real-time]
...
✅ Tailoring completed for google_a1b2c3

[2/3] Processing: microsoft_x9y8z7
...

Continue to next step (Build PDFs)? [Y/n]:
```

### Step 4: Build PDFs

The build step:
1. For each tailored resume:
2. Compiles LaTeX to PDF
3. Runs pdflatex twice (for references)
4. Moves artifacts to `build/` folder
5. Keeps final PDF in resume folder
6. Shows completion summary

**What you'll see:**
```
============================================================
📄 STEP 4: BUILD PDF RESUMES
============================================================
Building PDFs for 3 resumes

[1/3] Building: google_a1b2c3
🔨 Compiling LaTeX...
✅ PDF created: resumes/Data Scientist/google_a1b2c3/resume.pdf

[2/3] Building: microsoft_x9y8z7
...

============================================================
🎉 WORKFLOW COMPLETED!
============================================================
✅ Processed 3 resumes

📂 Resume locations:
   - resumes/Data Scientist/google_a1b2c3/resume.pdf
   - resumes/Data Scientist/microsoft_x9y8z7/resume.pdf
   - resumes/Data Scientist/netflix_p0q1r2/resume.pdf

✨ All done! Your tailored resumes are ready.
```

## State Management

The workflow automatically saves progress after each step to `.workflow_state.json`:

```json
{
  "completed_steps": [
    "step1_job_search",
    "step2_folder_creation"
  ],
  "data": {
    "job_search_output": "job_search_output/2025-09-29/data_scientist_143022.json",
    "created_folders": [
      "resumes/Data Scientist/google_a1b2c3",
      "resumes/Data Scientist/meta_d4e5f6"
    ],
    "job_title": "Data Scientist"
  }
}
```

If interrupted, resume with:
```bash
python run_workflow.py --config data_scientist_remote --resume
```

## Creating Your Own Configuration

1. Open `workflow_config.yaml`
2. Add a new configuration under `configs:`
3. Copy an existing config as a template
4. Modify the parameters
5. Run with your new config name

**Example:**

```yaml
configs:
  # Your new config
  senior_swe_bay_area:
    name: "Senior Software Engineer - Bay Area"
    description: "SWE roles in SF Bay Area"

    job_search:
      enabled: true
      title: "Senior Software Engineer"
      location: "San Francisco Bay Area"
      num_results: 15
      filters:
        job_type: ["Full-time"]
        seniority_level: ["Senior", "Lead"]

    # ... rest of config
```

Then run:
```bash
python run_workflow.py --config senior_swe_bay_area
```

## Advanced Features

### Aggressive Mode (No Confirmations)

For fully automated runs, disable confirmations:

```yaml
workflow:
  confirmations:
    after_search: true  # Still review job results
    after_folder_creation: false
    after_tailoring: false
    after_build: true  # Final review
```

### Auto Job Selection

Automatically select jobs based on criteria:

```yaml
folder_creation:
  selection_mode: "auto"
  auto_selection:
    max_applicants: 50  # Only jobs with < 50 applicants
    required_keywords:
      - "python"
      - "remote"
```

### Continue on Error

Keep processing even if one resume fails:

```yaml
workflow:
  continue_on_error: true
```

### Debug Mode

Get detailed logging:

```yaml
logging:
  level: "DEBUG"
  file: "logs/workflow_{timestamp}.log"
  console: true
```

## Troubleshooting

### Workflow Stuck or Interrupted

```bash
# Resume from last saved state
python run_workflow.py --config your_config --resume

# Or start from specific step
python run_workflow.py --config your_config --resume-from step3

# Or start fresh (clears state)
rm .workflow_state.json
python run_workflow.py --config your_config
```

### No Jobs Found

- Check your search parameters (title, location, keywords)
- Increase `num_results`
- Adjust filters (seniority_level, job_type)

### AI Tailoring Fails

- Ensure Claude CLI is installed and authenticated
- Check that resume folder has `job_details.json`
- Check that `sections/` folder exists with `.tex` files
- Review logs for specific errors

### PDF Build Fails

- Ensure pdflatex is installed (`which pdflatex`)
- Check LaTeX syntax in `.tex` files
- Review build logs in `build/` folder

### Permission Errors

```bash
# Make scripts executable
chmod +x build.sh create_job_folder.sh new_resume.sh
chmod +x fetch_job/job_search.py fetch_job/run.sh
chmod +x run_workflow.py resume_ai_creator.py
```

## Tips & Best Practices

1. **Start Small**: Begin with `num_results: 5` to test the workflow
2. **Review Job Listings**: Always confirm after job search to filter manually
3. **Check AI Output**: Review tailored resumes before building PDFs
4. **Keep Default Template Updated**: Your default template is the base for all resumes
5. **Use Meaningful Config Names**: Name configs by role and location
6. **Save Logs**: Keep logs for debugging and tracking applications
7. **Version Control**: Commit your configs to track changes
8. **Backup Resumes**: Keep generated resumes under version control

## Next Steps

After generating resumes:

1. **Review & Edit**: Manually review AI-tailored content
2. **Customize Further**: Add specific achievements for each company
3. **Update Cover Letters**: Create matching cover letters
4. **Track Applications**: Keep a spreadsheet of applications
5. **Follow Up**: Set reminders for follow-ups

## FAQ

**Q: Can I skip certain steps?**
A: Yes, set `enabled: false` for any step in the config.

**Q: Can I run multiple configs in parallel?**
A: Not recommended. Run them sequentially to avoid conflicts.

**Q: How do I update the default resume template?**
A: Edit files in `resumes/default/sections/` and `resumes/default/resume.tex`

**Q: Can I use a different AI model?**
A: Yes, modify `ai_config.model` in the config (must be supported by Claude CLI)

**Q: Where are logs stored?**
A: Check `logs/` folder (configurable in `logging.file`)

**Q: Can I export to other formats besides PDF?**
A: Currently only PDF. Modify `build.sh` for other formats.

## Related Documentation

- [README.md](README.md) - Main project documentation
- [job_prompt.jinja](job_prompt.jinja) - AI prompt template
- [workflow_config.yaml](workflow_config.yaml) - Configuration examples