#!/bin/bash

# Create Job Folder Script
# Creates a new resume variant for a specific job from job search JSON output
# Usage: ./create_job_folder.sh --json_path /path/to/job_search_output.json

set -e  # Exit on any error

# Default values
JSON_PATH=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --json_path)
            JSON_PATH="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 --json_path <path_to_json_file>"
            echo "Example: $0 --json_path /Users/rakshitmakan/Documents/Resume/job_search_output/2025-09-19/senior_agent_ai_engineer_004720.json"
            echo ""
            echo "This script:"
            echo "1. Reads job search JSON output"
            echo "2. Prompts you to select job(s) from the results:"
            echo "   - Single job: Enter job number (e.g., 3)"
            echo "   - Multiple jobs: Enter comma-separated numbers (e.g., 1,2,4)"
            echo "   - All jobs: Enter 'all'"
            echo "3. Creates new resume variants using new_resume.sh for each selected job"
            echo "4. Saves job details to a JSON file in each resume folder"
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
if [[ -z "$JSON_PATH" ]]; then
    echo "❌ Error: --json_path parameter is required"
    echo "Usage: $0 --json_path <path_to_json_file>"
    echo "Example: $0 --json_path /Users/rakshitmakan/Documents/Resume/job_search_output/2025-09-19/senior_agent_ai_engineer_004720.json"
    exit 1
fi

# Check if JSON file exists
if [[ ! -f "$JSON_PATH" ]]; then
    echo "❌ Error: JSON file not found at '$JSON_PATH'"
    exit 1
fi

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "❌ Error: jq is required but not installed"
    echo "Please install jq: brew install jq (on macOS) or apt-get install jq (on Ubuntu)"
    exit 1
fi

echo "📋 Reading job search results from JSON file..."

# Extract metadata
SEARCH_TITLE=$(jq -r '.metadata.job_title' "$JSON_PATH")
if [[ "$SEARCH_TITLE" == "null" ]]; then
    echo "❌ Error: Could not extract job title from JSON metadata"
    exit 1
fi

# Get number of jobs
JOB_COUNT=$(jq '.jobs | length' "$JSON_PATH")
if [[ "$JOB_COUNT" == "0" ]]; then
    echo "❌ Error: No jobs found in the JSON file"
    exit 1
fi

echo "🔍 Found $JOB_COUNT jobs for search: '$SEARCH_TITLE'"
echo ""
echo "📋 Available jobs:"

# Display jobs with index
for i in $(seq 0 $((JOB_COUNT - 1))); do
    TITLE=$(jq -r ".jobs[$i].title" "$JSON_PATH")
    COMPANY=$(jq -r ".jobs[$i].company" "$JSON_PATH")
    LOCATION=$(jq -r ".jobs[$i].location" "$JSON_PATH")
    APPLICANTS=$(jq -r ".jobs[$i].applicants" "$JSON_PATH")

    echo "$((i + 1)). $TITLE"
    echo "   Company: $COMPANY"
    echo "   Location: $LOCATION"
    echo "   Applicants: $APPLICANTS"
    echo ""
done

# Prompt user to select a job
echo -n "🎯 Select job number (1-$JOB_COUNT), multiple jobs (e.g., 1,2,3), or 'all': "
read -r JOB_SELECTION

# Function to process a single job
process_job() {
    local JOB_INDEX=$1

    # Extract selected job details
    local SELECTED_TITLE=$(jq -r ".jobs[$JOB_INDEX].title" "$JSON_PATH")
    local SELECTED_COMPANY=$(jq -r ".jobs[$JOB_INDEX].company" "$JSON_PATH")
    local SELECTED_DESCRIPTION=$(jq -r ".jobs[$JOB_INDEX].job_description" "$JSON_PATH")
    local SELECTED_LOCATION=$(jq -r ".jobs[$JOB_INDEX].location" "$JSON_PATH")
    local SELECTED_LINK=$(jq -r ".jobs[$JOB_INDEX].link" "$JSON_PATH")
    local SELECTED_APPLICANTS=$(jq -r ".jobs[$JOB_INDEX].applicants" "$JSON_PATH")
    local SELECTED_SALARY=$(jq -r ".jobs[$JOB_INDEX].salary_range" "$JSON_PATH")
    local SELECTED_JOB_TYPE=$(jq -r ".jobs[$JOB_INDEX].job_type" "$JSON_PATH")
    local SELECTED_SENIORITY=$(jq -r ".jobs[$JOB_INDEX].seniority_level" "$JSON_PATH")
    local SELECTED_SKILLS=$(jq -r ".jobs[$JOB_INDEX].skills_required" "$JSON_PATH")

    echo ""
    echo "✅ Processing job $((JOB_INDEX + 1)):"
    echo "   Title: $SELECTED_TITLE"
    echo "   Company: $SELECTED_COMPANY"
    echo "   Location: $SELECTED_LOCATION"

    # Clean company name for folder creation (remove special characters, convert to lowercase)
    local CLEAN_COMPANY=$(echo "$SELECTED_COMPANY" | sed 's/[^a-zA-Z0-9]/_/g' | tr '[:upper:]' '[:lower:]' | sed 's/__*/_/g' | sed 's/^_\|_$//g')

    # Generate unique hex identifier from job details to prevent conflicts
    local UNIQUE_DATA="${SELECTED_TITLE}_${SELECTED_COMPANY}_${SELECTED_LOCATION}_$(echo "$SELECTED_DESCRIPTION" | head -c 100)"
    local HEX_ID=$(echo -n "$UNIQUE_DATA" | openssl dgst -md5 -hex | cut -d' ' -f2 | head -c 6)

    # Append hex code to company name for uniqueness
    local FOLDER_NAME="${CLEAN_COMPANY}_${HEX_ID}"

    echo "📁 Creating resume folder for: $SEARCH_TITLE / $FOLDER_NAME"

    # Create new resume using new_resume.sh
    echo "🚀 Running: ./new_resume.sh --title \"$SEARCH_TITLE\" --name \"$FOLDER_NAME\""
    "$SCRIPT_DIR/new_resume.sh" --title "$SEARCH_TITLE" --name "$FOLDER_NAME"

    # Create job details JSON file
    local RESUME_PATH="$SCRIPT_DIR/resumes/$SEARCH_TITLE/$FOLDER_NAME"
    local JOB_DETAILS_FILE="$RESUME_PATH/job_details.json"

    echo "💾 Saving job details to: $JOB_DETAILS_FILE"

    # Create job details JSON using jq to ensure proper formatting
    jq -n \
      --arg job_title "$SELECTED_TITLE" \
      --arg company_name "$SELECTED_COMPANY" \
      --arg job_description "$SELECTED_DESCRIPTION" \
      --arg location "$SELECTED_LOCATION" \
      --arg job_link "$SELECTED_LINK" \
      --arg applicants "$SELECTED_APPLICANTS" \
      --arg salary_range "$SELECTED_SALARY" \
      --arg job_type "$SELECTED_JOB_TYPE" \
      --arg seniority_level "$SELECTED_SENIORITY" \
      --arg skills_required "$SELECTED_SKILLS" \
      --arg source_search_title "$SEARCH_TITLE" \
      --arg created_at "$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")" \
      --arg source_json_file "$JSON_PATH" \
      '{
        job_title: $job_title,
        company_name: $company_name,
        job_description: $job_description,
        location: $location,
        job_link: $job_link,
        applicants: $applicants,
        salary_range: $salary_range,
        job_type: $job_type,
        seniority_level: $seniority_level,
        skills_required: $skills_required,
        source_search_title: $source_search_title,
        created_at: $created_at,
        source_json_file: $source_json_file
      }' > "$JOB_DETAILS_FILE"

    echo "✅ Successfully created job application folder for $SELECTED_COMPANY!"
    echo "📂 Resume folder: resumes/$SEARCH_TITLE/$FOLDER_NAME/"
    echo "📄 Job details saved: job_details.json"
}

# Parse and validate selection
if [[ "$JOB_SELECTION" == "all" ]]; then
    # Process all jobs
    echo "🔄 Processing all $JOB_COUNT jobs..."
    for i in $(seq 0 $((JOB_COUNT - 1))); do
        process_job $i
    done
elif [[ "$JOB_SELECTION" =~ ^[0-9,]+$ ]]; then
    # Handle multiple job numbers (comma-separated)
    IFS=',' read -ra JOB_NUMBERS <<< "$JOB_SELECTION"

    # Validate each job number
    for job_num in "${JOB_NUMBERS[@]}"; do
        job_num=$(echo "$job_num" | xargs)  # Trim whitespace
        if ! [[ "$job_num" =~ ^[0-9]+$ ]] || [[ "$job_num" -lt 1 ]] || [[ "$job_num" -gt "$JOB_COUNT" ]]; then
            echo "❌ Error: Invalid job number '$job_num'. Please enter numbers between 1 and $JOB_COUNT"
            exit 1
        fi
    done

    # Process each selected job
    echo "🔄 Processing ${#JOB_NUMBERS[@]} selected jobs..."
    for job_num in "${JOB_NUMBERS[@]}"; do
        job_num=$(echo "$job_num" | xargs)  # Trim whitespace
        JOB_INDEX=$((job_num - 1))
        process_job $JOB_INDEX
    done
elif [[ "$JOB_SELECTION" =~ ^[0-9]+$ ]]; then
    # Handle single job number
    if [[ "$JOB_SELECTION" -lt 1 ]] || [[ "$JOB_SELECTION" -gt "$JOB_COUNT" ]]; then
        echo "❌ Error: Invalid selection. Please enter a number between 1 and $JOB_COUNT, multiple numbers (e.g., 1,2,3), or 'all'"
        exit 1
    fi

    # Process single job
    JOB_INDEX=$((JOB_SELECTION - 1))
    process_job $JOB_INDEX
else
    echo "❌ Error: Invalid selection '$JOB_SELECTION'. Please enter:"
    echo "   - A single job number (1-$JOB_COUNT)"
    echo "   - Multiple job numbers separated by commas (e.g., 1,2,3)"
    echo "   - 'all' to process all jobs"
    exit 1
fi

echo ""
echo "🔧 Next steps:"
echo "1. Customize your resume sections in the created folders under: resumes/$SEARCH_TITLE/"
echo "2. Build your resume(s): ./build.sh --title \"$SEARCH_TITLE\" --path \"<company_name>\""
echo "3. Review job details in each folder's job_details.json file"
echo ""
echo "💡 Tip: Tailor your resume based on the job description and required skills for each application!"