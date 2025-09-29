# Test Configs Quick Reference

Quick reference for the 4 test configurations.

## 🎯 Which Test Config Should I Use?

| Goal | Config | Time | Command |
|------|--------|------|---------|
| Test everything end-to-end | `test_minimal` | 3-5 min | `python run_workflow.py --config test_minimal` |
| Test search + folders only | `test_search_only` | 30-60 sec | `python run_workflow.py --config test_search_only` |
| Test AI tailoring only | `test_ai_only` | 1-2 min | `python run_workflow.py --config test_ai_only` |
| Validate config syntax | `test_dry_run` | < 10 sec | `python run_workflow.py --config test_dry_run` |

---

## Test Config Details

### 1️⃣ test_minimal (⭐ Recommended)

```yaml
Job Search: 3 Data Scientist jobs (Remote)
Folder Creation: Manual selection (you pick 1)
AI Tailoring: 2 sections only (skills + summary)
Build: Yes (full PDF compilation)
Time: 3-5 minutes
```

**Perfect for:**
- First-time testing
- Verifying end-to-end workflow
- Testing with minimal resources

**Run it:**
```bash
poetry run python run_workflow.py --config test_minimal

# When prompted:
# - Review 3 jobs → Press Y
# - Select job → Type "1"
# - After folders → Press Y
# - After AI → Press Y
# - After build → Done!
```

---

### 2️⃣ test_search_only (⚡ Fast)

```yaml
Job Search: 3 Software Engineer jobs (Remote)
Folder Creation: Manual selection
AI Tailoring: DISABLED
Build: DISABLED
Time: 30-60 seconds
```

**Perfect for:**
- Quick smoke test
- Testing job search API
- Verifying folder creation
- Testing without AI or LaTeX dependencies

**Run it:**
```bash
poetry run python run_workflow.py --config test_search_only

# Results in:
# - job_search_output/YYYY-MM-DD/*.json
# - resumes/Software Engineer/company_xxxxx/
```

---

### 3️⃣ test_ai_only (🤖 AI Only)

```yaml
Job Search: DISABLED
Folder Creation: DISABLED
AI Tailoring: 1 section only (skills)
Build: DISABLED
Time: 1-2 minutes per folder
```

**Perfect for:**
- Testing AI tailoring in isolation
- Debugging prompt issues
- Testing Claude CLI integration

**Prerequisites:**
- Existing resume folder with job_details.json

**Run it:**
```bash
# Use existing folder from previous test
poetry run python run_workflow.py --config test_ai_only
```

**Note:** Requires manual state setup. Better to use `test_minimal` for most testing.

---

### 4️⃣ test_dry_run (✅ Validation)

```yaml
Job Search: Minimal config
Folder Creation: Minimal config
AI Tailoring: Minimal config
Build: Minimal config
Execution: NONE (validation only)
Time: < 10 seconds
```

**Perfect for:**
- Validating YAML syntax
- Testing config changes
- Checking file paths
- CI/CD pipeline validation

**Run it:**
```bash
poetry run python run_workflow.py --config test_dry_run
```

---

## Comparison Table

| Feature | test_minimal | test_search_only | test_ai_only | test_dry_run |
|---------|--------------|------------------|--------------|--------------|
| **Job Search** | ✅ 3 jobs | ✅ 3 jobs | ❌ | ✅ Config only |
| **Folder Creation** | ✅ Manual | ✅ Manual | ❌ | ✅ Config only |
| **AI Tailoring** | ✅ 2 sections | ❌ | ✅ 1 section | ✅ Config only |
| **PDF Build** | ✅ Full | ❌ | ❌ | ✅ Config only |
| **Requires Claude CLI** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Requires LaTeX** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Requires Internet** | ✅ Yes | ✅ Yes | ❌ No* | ❌ No |
| **Creates Files** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Use for CI/CD** | ❌ No | ⚠️ Maybe | ❌ No | ✅ Yes |
| **Time** | 3-5 min | 30-60 sec | 1-2 min | < 10 sec |

\* Requires internet if job_details.json needs job description

---

## Quick Testing Workflow

### First Time Setup
```bash
# 1. Install
poetry install

# 2. Verify
poetry run python run_workflow.py --list-configs

# 3. Test
poetry run python run_workflow.py --config test_minimal
```

### Regular Testing
```bash
# Quick test (no AI)
poetry run python run_workflow.py --config test_search_only

# Full test (with AI)
poetry run python run_workflow.py --config test_minimal
```

### After Making Changes
```bash
# 1. Validate config
poetry run python run_workflow.py --config test_dry_run

# 2. Test end-to-end
poetry run python run_workflow.py --config test_minimal
```

---

## Configuration Highlights

### test_minimal
```yaml
num_results: 3                    # Only 3 jobs
selection_mode: "manual"           # You pick 1
sections_to_tailor: ["skills", "summary"]  # Just 2 sections
verbose: false                     # Less output
state_file: ".workflow_state_test.json"  # Separate state
```

### test_search_only
```yaml
ai_tailoring:
  enabled: false                   # Skip AI
build:
  enabled: false                   # Skip build
continue_on_error: true            # Continue if errors
```

### test_ai_only
```yaml
job_search:
  enabled: false                   # Skip search
folder_creation:
  enabled: false                   # Skip folders
sections_to_tailor: ["skills"]    # Just 1 section
```

### test_dry_run
```yaml
num_results: 1                     # Minimal
save_state: false                  # No state file
# Everything enabled but won't execute
```

---

## Expected Output

### test_minimal
```
📋 STEP 1: JOB SEARCH
🔍 Running job search...
✅ Job search completed
📊 Found 3 jobs
Continue? [Y/n]: y

📁 STEP 2: FOLDER CREATION
🎯 Select job number (1-3): 1
✅ Created 1 resume folders

🤖 STEP 3: AI RESUME TAILORING
[1/1] Processing: google_a1b2c3
✅ Tailoring completed

📄 STEP 4: BUILD PDF RESUMES
[1/1] Building: google_a1b2c3
✅ PDF created: resumes/Data Scientist/google_a1b2c3/resume.pdf

🎉 WORKFLOW COMPLETED!
```

### test_search_only
```
📋 STEP 1: JOB SEARCH
✅ Job search completed
📊 Found 3 jobs

📁 STEP 2: FOLDER CREATION
🎯 Select job number (1-3): 1,2
✅ Created 2 resume folders

⏭️  Step 3 (AI Tailoring) disabled, skipping...
⏭️  Step 4 (Build PDFs) disabled, skipping...

✨ All done!
```

---

## Troubleshooting

### "Module 'yaml' not found"
```bash
poetry install
```

### "Config not found"
```bash
poetry run python run_workflow.py --list-configs
```

### Job search fails
```bash
# Test job search directly
cd fetch_job
python job_search.py --title "Test" --location "Remote" --num-results 1
```

### AI tailoring fails
```bash
# Check Claude CLI
which claude
claude --version
```

### PDF build fails
```bash
# Check pdflatex
which pdflatex

# Test build directly
./build.sh --title "Data Scientist" --path "test_folder"
```

---

## Files Created by Tests

### test_minimal
- `job_search_output/YYYY-MM-DD/data_scientist_*.json`
- `resumes/Data Scientist/company_xxxxx/`
- `resumes/Data Scientist/company_xxxxx/resume.pdf`
- `.workflow_state_test.json`
- `logs/test_workflow_*.log`

### test_search_only
- `job_search_output/YYYY-MM-DD/software_engineer_*.json`
- `resumes/Software Engineer/company_xxxxx/`
- `.workflow_state_search_test.json`
- `logs/test_search_*.log`

### test_ai_only
- Modified `.tex` files in sections/
- `claude_response.json`
- `logs/test_ai_*.log`

### test_dry_run
- None (validation only)

---

## Cleanup

```bash
# Remove test state files
rm .workflow_state_test.json .workflow_state_search_test.json

# Remove test logs
rm -rf logs/test_*.log

# Remove test resumes (optional)
rm -rf resumes/Data\ Scientist/
rm -rf resumes/Software\ Engineer/

# Remove test job searches (optional)
rm -rf job_search_output/
```

---

## Next Steps

After successful testing:

1. ✅ Create your own production config
2. ✅ Increase `num_results` (e.g., 20)
3. ✅ Enable all sections for AI tailoring
4. ✅ Run with real job searches
5. ✅ Review and customize AI output
6. ✅ Submit applications!

---

📖 **Full Documentation:** [WORKFLOW.md](WORKFLOW.md)
🧪 **Testing Guide:** [TEST_GUIDE.md](TEST_GUIDE.md)
📚 **Main README:** [README.md](README.md)