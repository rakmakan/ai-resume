# Testing Guide

Quick guide for testing the AI Resume Workflow system.

## Available Test Configurations

### 1. `test_minimal` - Full Workflow Test (Recommended)

**What it does:**
- Searches for 3 Data Scientist jobs
- Lets you manually select 1 job
- AI tailors only 2 sections (skills + summary)
- Builds PDF

**Estimated time:** 3-5 minutes

**Usage:**
```bash
python run_workflow.py --config test_minimal
```

**What to expect:**
1. Searches LinkedIn for 3 remote Data Scientist positions
2. Shows you the 3 jobs found
3. You select 1 job (type `1` and press Enter)
4. AI tailors the skills and summary sections
5. Builds a PDF

**Tips:**
- Select job with fewer applicants for testing
- Check `logs/test_workflow_*.log` for detailed output
- Resume folder created under `resumes/Data Scientist/`

---

### 2. `test_search_only` - Quick Search Test

**What it does:**
- Searches for 3 Software Engineer jobs
- Creates resume folders
- **Skips AI tailoring and PDF build**

**Estimated time:** 30-60 seconds

**Usage:**
```bash
python run_workflow.py --config test_search_only
```

**Use this to test:**
- Job search functionality
- Folder creation logic
- Config parsing
- State management

**What to check:**
- `job_search_output/` has new JSON file
- `resumes/Software Engineer/` has new folders
- Each folder has `job_details.json`
- `.workflow_state_search_test.json` created

---

### 3. `test_ai_only` - AI Tailoring Test

**What it does:**
- **Skips job search and folder creation**
- Tests AI tailoring on existing resume folder
- Only tailors the skills section

**Estimated time:** 1-2 minutes per folder

**Prerequisites:**
- You must have an existing resume folder
- Example: `resumes/Data Scientist/cogeco_connexion_f313b1/`

**Usage:**
```bash
# First, manually edit .workflow_state.json to set folders
# Or run test_search_only first, then run:
python run_workflow.py --config test_ai_only
```

**Note:** This config is for isolated AI testing. For full workflow testing, use `test_minimal` instead.

---

### 4. `test_dry_run` - Config Validation

**What it does:**
- Validates configuration structure
- Checks all file paths exist
- Tests orchestrator initialization
- **Doesn't execute any real work**

**Estimated time:** < 10 seconds

**Usage:**
```bash
python run_workflow.py --config test_dry_run
```

**Use this to:**
- Verify YAML syntax is correct
- Check script paths are valid
- Test new configuration changes
- Validate orchestrator logic

---

## Quick Testing Workflow

### First Time Setup

```bash
# 1. Install dependencies
poetry install

# 2. Verify default template exists
ls -la resumes/default/

# 3. Check scripts are executable
ls -la *.sh fetch_job/*.py *.py

# 4. List all configs
python run_workflow.py --list-configs
```

### Run Quick Test

```bash
# Test the entire workflow (recommended)
python run_workflow.py --config test_minimal

# You'll be prompted at each step:
# - After job search: Review 3 jobs, press Y
# - Select job: Type "1" to select first job
# - After folder creation: Press Y
# - After AI tailoring: Press Y
# - After PDF build: Done!

# Check results
ls resumes/Data\ Scientist/*/resume.pdf
```

### Test Individual Components

```bash
# Test job search + folder creation only (fast)
python run_workflow.py --config test_search_only

# Test config validation only (very fast)
python run_workflow.py --config test_dry_run
```

### Resume from Interruption

```bash
# If you interrupt test_minimal, resume with:
python run_workflow.py --config test_minimal --resume

# Or resume from specific step:
python run_workflow.py --config test_minimal --resume-from step3
```

---

## Debugging Tests

### Check Logs

```bash
# View latest test log
tail -f logs/test_workflow_*.log

# View specific test log
cat logs/test_workflow_20250929_143022.log

# View search-only test log
cat logs/test_search_*.log
```

### Check State Files

```bash
# View test state
cat .workflow_state_test.json

# View search test state
cat .workflow_state_search_test.json

# Clean up test states
rm .workflow_state_test.json .workflow_state_search_test.json
```

### Check Generated Files

```bash
# Check job search output
ls -lht job_search_output/*/
cat job_search_output/2025-09-29/*.json | jq '.metadata'

# Check created folders
ls -la resumes/Data\ Scientist/
ls -la resumes/Software\ Engineer/

# Check specific resume folder
ls -la resumes/Data\ Scientist/google_a1b2c3/
cat resumes/Data\ Scientist/google_a1b2c3/job_details.json | jq
```

### Verify PDF Build

```bash
# Check if PDF was generated
find resumes -name "resume.pdf" -mmin -10

# Open PDF
open "resumes/Data Scientist/google_a1b2c3/resume.pdf"
```

---

## Common Issues & Solutions

### Issue: "Config 'test_minimal' not found"

**Solution:**
```bash
# Verify workflow_config.yaml exists
ls -la workflow_config.yaml

# List available configs
python run_workflow.py --list-configs
```

### Issue: Job search finds 0 jobs

**Solution:**
- Job search API might be rate-limited
- Try broader search criteria
- Check `logs/` for errors
- Verify `fetch_job/job_search.py` works:
  ```bash
  cd fetch_job
  python job_search.py --title "Data Scientist" --location "Remote" --num-results 3
  ```

### Issue: "Default template not found"

**Solution:**
```bash
# Check if default template exists
ls -la resumes/default/

# If missing, create it or clone from existing
cp -r "resumes/Data Scientist/cogeco_connexion_f313b1" resumes/default
```

### Issue: AI tailoring fails

**Solution:**
- Verify Claude CLI is installed: `which claude`
- Check authentication: `claude --version`
- Check resume folder has all required files:
  ```bash
  ls -la resumes/Data\ Scientist/*/
  ls -la resumes/Data\ Scientist/*/sections/
  ```
- Check `job_details.json` exists and is valid JSON:
  ```bash
  cat resumes/Data\ Scientist/*/job_details.json | jq
  ```

### Issue: PDF build fails

**Solution:**
- Check pdflatex is installed: `which pdflatex`
- Test build manually:
  ```bash
  ./build.sh --title "Data Scientist" --path "google_a1b2c3"
  ```
- Check LaTeX syntax in `.tex` files
- Review build logs in `build/` folder

### Issue: Permission denied

**Solution:**
```bash
# Make all scripts executable
chmod +x *.sh *.py
chmod +x fetch_job/*.sh fetch_job/*.py
```

---

## Test Checklist

Use this checklist to verify everything works:

- [ ] **Setup**
  - [ ] Dependencies installed (`poetry install`)
  - [ ] Default template exists (`resumes/default/`)
  - [ ] Scripts are executable
  - [ ] Claude CLI authenticated

- [ ] **Config Loading**
  - [ ] List configs works (`--list-configs`)
  - [ ] Test configs appear in list
  - [ ] YAML syntax is valid

- [ ] **Job Search (test_search_only)**
  - [ ] Searches and finds jobs
  - [ ] Creates JSON output file
  - [ ] JSON contains job metadata
  - [ ] No errors in logs

- [ ] **Folder Creation (test_search_only)**
  - [ ] Creates resume folders
  - [ ] Copies template files
  - [ ] Creates `job_details.json`
  - [ ] Folders have correct structure

- [ ] **AI Tailoring (test_minimal)**
  - [ ] Reads job details
  - [ ] Calls Claude CLI
  - [ ] Modifies `.tex` files
  - [ ] Creates `claude_response.json`
  - [ ] No errors in AI output

- [ ] **PDF Build (test_minimal)**
  - [ ] Compiles LaTeX successfully
  - [ ] Generates `resume.pdf`
  - [ ] PDF opens correctly
  - [ ] Content looks correct

- [ ] **Workflow Control**
  - [ ] Confirmations work at each step
  - [ ] Can interrupt with Ctrl+C
  - [ ] State is saved correctly
  - [ ] Resume works (`--resume`)
  - [ ] Resume from step works (`--resume-from step3`)

- [ ] **Error Handling**
  - [ ] Graceful error messages
  - [ ] Logs capture errors
  - [ ] Can continue on error (if enabled)

- [ ] **Cleanup**
  - [ ] Build artifacts moved to `build/`
  - [ ] Logs created in `logs/`
  - [ ] State files created
  - [ ] No leftover temp files

---

## Performance Benchmarks

Expected execution times on typical hardware:

| Config | Steps | Time | Notes |
|--------|-------|------|-------|
| `test_minimal` | All 4 | 3-5 min | Full workflow, 1 job |
| `test_search_only` | 1-2 | 30-60 sec | No AI or build |
| `test_ai_only` | 3 only | 1-2 min | Per folder |
| `test_dry_run` | 0 | < 10 sec | Validation only |

---

## Next Steps After Testing

Once all tests pass:

1. **Create your own config** in `workflow_config.yaml`
2. **Run with real parameters** (more jobs, all sections)
3. **Review AI output** before submitting resumes
4. **Customize prompts** in `job_prompt.jinja` if needed
5. **Set up logging** for tracking applications

---

## Getting Help

If tests fail:

1. Check logs in `logs/test_*.log`
2. Review [WORKFLOW.md](WORKFLOW.md) for detailed documentation
3. Verify prerequisites (Poetry, Claude CLI, pdflatex)
4. Check individual scripts work manually
5. Open an issue with error logs