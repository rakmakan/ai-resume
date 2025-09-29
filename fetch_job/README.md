# Job Search Tool

An advanced interactive CLI tool for finding job opportunities with low applicant counts and comprehensive job details. Outputs results in both CSV and JSON formats.

## 🌟 Features

### Core Functionality
- 🔍 **Interactive command-line interface** with smart prompts
- 👥 **Filter jobs by applicant count** (≤10 by default for better chances)
- 📍 **Location-based search** (city names, "Remote", or worldwide)
- 💼 **Experience level filtering** with auto-enhanced keywords
- 📊 **Dual output formats** - CSV and JSON with timestamps and metadata
- 📁 **Automatic directory organization** by date

### Advanced Job Details
- 📝 **Full job descriptions** extracted from LinkedIn postings
- 🛠️ **Skills and requirements** identification
- 💰 **Salary information** (when available)
- 🏢 **Job type** (Full-time, Part-time, Contract, etc.)
- 📈 **Seniority level** (Entry, Mid, Senior, Executive)
- 🏭 **Industry and company insights**
- 📊 **Dual search modes**: Basic (fast) vs Detailed (comprehensive)

## 🚀 Quick Start

### Easy Setup
```bash
# Run the automated setup
./setup.sh

# Or use the convenient run script
./run.sh
```

### Manual Installation

#### Using uv (Recommended)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run setup
./setup.sh
```

#### Using pip
```bash
cd fetch_job
pip install requests beautifulsoup4 lxml
```

## 🎯 Usage

### Quick Start
```bash
# Easy way - handles everything automatically
./run.sh

# Manual way
./job_search.py
```

### Interactive Prompts
The tool will ask you for:
- 📋 **Job title** (e.g., "Software Engineer", "Data Scientist")
- 💼 **Years of experience** (0-20+, or leave blank for any)
- 📍 **Location** (e.g., "San Francisco", "Remote", or leave blank for any)
- 👥 **Maximum applicants** (default: 10 for lower competition)
- 🔍 **Maximum results** to find (default: 50)
- 📖 **Search mode**: Basic (fast) or Detailed (includes full job descriptions)

## 📊 Output & Results

### File Organization
Results are automatically saved in both CSV and JSON formats:
```
../job_search_output/
└── YYYY-MM-DD/
    ├── job_title_HHMMSS.csv
    └── job_title_HHMMSS.json
```

Example:
```
../job_search_output/
└── 2025-01-19/
    ├── data_scientist_143022.csv
    └── data_scientist_143022.json
```

### 📈 Data Structure

#### CSV Format
Standard spreadsheet format with headers and metadata comments:

**Basic Mode (15 fields)**
- **title**: Job title
- **company**: Company name
- **location**: Job location
- **link**: Direct link to job posting
- **job_id**: LinkedIn job identifier
- **applicants**: Number of applicants (when available)
- **posting_date**: When the job was posted
- **source**: Job board source (LinkedIn)
- **scraped_at**: When the data was collected
- Plus placeholders for detailed fields

**Detailed Mode (15 fields with full data)**
All basic fields plus:
- **job_description**: 📝 Full job description and requirements
- **job_type**: 🏢 Employment type (Full-time, Part-time, Contract)
- **seniority_level**: 📈 Experience level (Entry, Mid-Senior, Director)
- **company_size**: 🏭 Company size information
- **industry**: 🏗️ Industry sector
- **skills_required**: 🛠️ Required skills and technologies
- **salary_range**: 💰 Salary information (when available)

#### JSON Format
Structured data format perfect for programmatic access:

```json
{
  "metadata": {
    "search_date": "2025-01-19 14:30:22",
    "job_title": "Software Engineer",
    "experience": "3",
    "location": "San Francisco",
    "max_applicants": 10,
    "total_results": 25,
    "search_mode": "Detailed"
  },
  "jobs": [
    {
      "title": "Senior Software Engineer",
      "company": "TechCorp",
      "location": "San Francisco, CA",
      "applicants": 7,
      "job_description": "Full job description here...",
      "skills_required": "Python, React, AWS",
      "salary_range": "$120,000 - $160,000",
      ...
    }
  ]
}
```

### 📋 File Metadata
Each file includes comprehensive metadata:
- Search parameters used
- Date and time of search
- Total results found
- Search criteria summary
- Search mode (Basic vs Detailed)

## 📝 Examples

### Software Engineer Search
```
🚀 Interactive Job Search Tool
==================================================
📋 What job title are you looking for? Software Engineer
💼 Years of experience: 3
📍 Location: San Francisco
👥 Maximum number of applicants: 5
🔍 Maximum number of jobs to find: 30

📖 Job Details Options:
   📋 Basic: Fast search, basic info only
   📝 Detailed: Slower search, includes full job descriptions and details
🔍 Fetch detailed job descriptions? y

🔍 Search Keywords: 'Software Engineer mid level'
▶️  Start search? y
```

### Data Scientist Remote Search (Detailed Mode)
```
🚀 Interactive Job Search Tool
==================================================
📋 What job title are you looking for? Data Scientist
💼 Years of experience:
📍 Location: Remote
👥 Maximum number of applicants: 10
🔍 Maximum number of jobs to find: 25

📖 Job Details Options:
🔍 Fetch detailed job descriptions? y

📋 Phase 1: Collecting job listings...
📖 Phase 2: Fetching detailed job descriptions for 8 jobs...
📄 1/8: Getting details for Senior Data Scientist at TechCorp
   ✅ Got full details for Senior Data Scientist
```

### Quick Basic Search
```
📋 What job title are you looking for? Product Manager
💼 Years of experience: 5
📍 Location: Toronto
🔍 Fetch detailed job descriptions? n

⚡ Fast search mode - basic information only
✅ 1. Senior Product Manager at StartupXYZ (3 applicants)
✅ 2. Product Manager - AI at BigTech (7 applicants)
```

## 💡 Tips for Better Results

### Search Optimization
1. **Use specific job titles**: "Software Engineer" vs "Engineer"
2. **Try different experience levels**: Some jobs are better suited for specific experience ranges
3. **Experiment with locations**: "Remote", city names, or leave blank for broader search
4. **Adjust applicant threshold**: Lower numbers (5-10) for less competition
5. **Run searches at different times**: Job postings vary throughout the day

### Mode Selection
6. **Choose Basic mode** for quick overviews and rapid job discovery
7. **Choose Detailed mode** when you need full job descriptions and comprehensive data
8. **Use Detailed mode sparingly** for jobs you're seriously considering (it's slower)

## 🧠 Smart Search Strategy

### Auto-Enhanced Keywords
The tool automatically enhances your search based on experience:
- **0 years**: Adds "entry level junior" keywords
- **1-2 years**: Adds "junior" keywords
- **3-5 years**: Adds "mid level" keywords
- **6-10 years**: Adds "senior" keywords
- **10+ years**: Adds "principal lead staff" keywords

### Two-Phase Process (Detailed Mode)
1. **Phase 1**: Rapid collection of job listings with basic info
2. **Phase 2**: Deep extraction of job descriptions and details

## ⚡ Performance & Rate Limiting

### Timing
- **Basic Mode**: ~30 seconds for 20 jobs
- **Detailed Mode**: ~3-5 minutes for 20 jobs (includes full descriptions)

### Built-in Protections
- **Rate limiting**: 1-4 second delays between requests
- **Respectful scraping**: Mimics human browsing behavior
- **Error handling**: Graceful fallbacks for failed requests
- **Anti-detection**: Modern browser headers and session management

## 🛠️ Troubleshooting

### Common Issues

1. **No results found**:
   - Try broader search terms (remove specific technologies)
   - Increase max applicants threshold (try 15-20)
   - Remove location restrictions (leave blank)
   - Adjust experience level (try one level lower/higher)

2. **Connection errors or 400/403 responses**:
   - Check internet connection
   - Wait 5-10 minutes before retrying
   - LinkedIn may be temporarily rate-limiting
   - Try using a VPN if consistently blocked

3. **Job descriptions not loading**:
   - Use Basic mode if Detailed mode fails
   - Some job posts may be private/expired
   - LinkedIn occasionally changes their page structure
   - Results will show "Could not fetch job description"

4. **Missing applicant counts**:
   - LinkedIn doesn't always show applicant counts
   - Jobs without counts are still included in results
   - Try running search at different times
   - Recent postings may not have applicant data yet

### Setup Issues

If you encounter import errors:
```bash
# Run the setup script (recommended)
./setup.sh

# Or install manually with uv
uv pip install requests beautifulsoup4 lxml

# Or with pip
pip install requests beautifulsoup4 lxml
```

If virtual environment issues:
```bash
# Remove and recreate
rm -rf .venv
./setup.sh
```

### Performance Issues

If searches are very slow:
- Use Basic mode for faster results
- Reduce max results (try 10-20 instead of 50)
- Search during off-peak hours
- Check your internet connection speed

## ⚖️ Legal & Ethical Considerations

### What This Tool Does
- ✅ **Accesses publicly available job postings** only
- ✅ **Includes respectful rate limiting** (1-4 second delays)
- ✅ **Does not store personal user data**
- ✅ **Uses standard web scraping practices**
- ✅ **Mimics normal browser behavior**

### Best Practices
- 🤝 **Respect rate limits** - don't run multiple instances
- 🕐 **Use sparingly** - avoid excessive daily searches
- 📋 **Follow website terms** - comply with LinkedIn's ToS
- 🎯 **Use responsibly** - for legitimate job searching only

### Disclaimer
This tool is for educational and personal job search purposes. Users are responsible for complying with all applicable terms of service and laws. Always respect website rate limits and robots.txt files.