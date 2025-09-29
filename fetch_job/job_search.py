#!/usr/bin/env python3
"""
Interactive Job Search CLI Tool
Search for jobs with low applicant counts and save results in organized CSV and JSON files.
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import random
from datetime import datetime
import sys
import os
import re
from pathlib import Path

class InteractiveJobSearcher:
    def __init__(self):
        self.session = requests.Session()
        # Use more realistic headers to avoid detection
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        ]
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
        })
        self.results = []

    def get_user_input(self):
        """Get job search parameters from user interactively."""
        print("🚀 Interactive Job Search Tool")
        print("=" * 50)

        # Get job title
        while True:
            job_title = input("📋 What job title are you looking for? (e.g., 'Software Engineer', 'Data Scientist'): ").strip()
            if job_title:
                break
            print("❌ Please enter a valid job title.")

        # Get years of experience
        while True:
            try:
                experience = input("💼 Years of experience (0-20+, or press Enter for any): ").strip()
                if not experience:
                    experience = None
                    break
                experience = int(experience)
                if 0 <= experience <= 30:
                    break
                else:
                    print("❌ Please enter a number between 0 and 30.")
            except ValueError:
                print("❌ Please enter a valid number or press Enter for any experience level.")

        # Get location with Canada support
        print("\n📍 Location Options:")
        print("   🍁 'Canada' - Search across Toronto, Vancouver, Calgary, Ottawa, Montreal")
        print("   🌍 Specific city - e.g., 'Toronto', 'Vancouver', 'Calgary'")
        print("   🏠 'Remote' - Remote positions")
        print("   ⏎ Press Enter for any location")

        location = input("📍 Location: ").strip()
        if not location:
            location = ""
        elif location.lower() == "canada":
            location = self.get_canadian_locations()

        # Additional filters
        print("\n⚙️  Additional Filters:")

        # Time filter
        print("\n⏰ Job Posting Time:")
        print("   1️⃣  Last 24 hours")
        print("   2️⃣  Last 48 hours (default)")
        print("   3️⃣  Last week")
        print("   4️⃣  Last 2 weeks")

        time_choice = input("⏰ Select time range (1-4, or press Enter for 48 hours): ").strip()
        time_filters = {
            '1': 'r86400',    # 24 hours
            '2': 'r172800',   # 48 hours
            '3': 'r604800',   # 1 week
            '4': 'r1209600',  # 2 weeks
        }
        time_filter = time_filters.get(time_choice, 'r172800')  # Default to 48 hours

        max_applicants = input("👥 Maximum number of applicants (default 10, press Enter to use default): ").strip()
        if not max_applicants:
            max_applicants = 10
        else:
            try:
                max_applicants = int(max_applicants)
            except ValueError:
                max_applicants = 10

        max_results = input("🔍 Maximum number of jobs to find (default 50, press Enter to use default): ").strip()
        if not max_results:
            max_results = 50
        else:
            try:
                max_results = int(max_results)
            except ValueError:
                max_results = 50

        # Ask about detailed job descriptions
        print("\n📖 Job Details Options:")
        print("   📋 Basic: Fast search, basic info only")
        print("   📝 Detailed: Slower search, includes full job descriptions and details")
        fetch_details = input("🔍 Fetch detailed job descriptions? (y/N): ").strip().lower()
        fetch_details = fetch_details in ['y', 'yes']

        return {
            'job_title': job_title,
            'experience': experience,
            'location': location,
            'time_filter': time_filter,
            'max_applicants': max_applicants,
            'max_results': max_results,
            'fetch_details': fetch_details
        }

    def get_canadian_locations(self):
        """Return list of major Canadian cities for comprehensive job search."""
        return ["Toronto, ON, Canada", "Vancouver, BC, Canada", "Calgary, AB, Canada",
                "Ottawa, ON, Canada", "Montreal, QC, Canada", "Edmonton, AB, Canada",
                "Winnipeg, MB, Canada", "Quebec City, QC, Canada", "Hamilton, ON, Canada",
                "Kitchener, ON, Canada"]

    def create_search_keywords(self, job_title, experience):
        """Create search keywords based on job title and experience."""
        # Use the job title as-is for better matching
        keywords = job_title

        # Don't append experience levels to keywords - LinkedIn handles this through filters
        # This prevents over-specific searches that return no results

        return keywords

    def is_job_relevant(self, job_title, search_keywords):
        """Check if a job title is actually relevant to the search keywords."""
        job_title_lower = job_title.lower()
        search_lower = search_keywords.lower()

        # For "Corporate Communications" search
        if 'corporate communications' in search_lower:
            # Relevant keywords for corporate communications
            relevant_keywords = [
                'communications', 'communication', 'corporate communications',
                'internal communications', 'external communications',
                'strategic communications', 'public relations', 'pr',
                'media relations', 'content strategy', 'brand communications',
                'marketing communications', 'marcom', 'corporate affairs'
            ]

            # Irrelevant keywords to exclude
            irrelevant_keywords = [
                'talent manager', 'people', 'culture', 'hr', 'human resources',
                'administrative assistant', 'admin', 'care facilitator',
                'case manager', 'events manager', 'retail', 'sales',
                'customer service', 'account manager'
            ]

            # Check if title contains irrelevant terms
            for irrelevant in irrelevant_keywords:
                if irrelevant in job_title_lower:
                    return False

            # Check if title contains relevant terms
            for relevant in relevant_keywords:
                if relevant in job_title_lower:
                    return True

            return False

        # For other job searches, be more permissive
        else:
            # Basic keyword matching for other job titles
            search_words = search_lower.split()
            title_words = job_title_lower.split()

            # At least 60% of search words should appear in job title
            matches = sum(1 for word in search_words if any(word in title_word for title_word in title_words))
            return matches >= len(search_words) * 0.6

    def search_linkedin_jobs(self, keywords, location="", max_applicants=10, max_results=50, time_filter='r172800'):
        """Search for jobs on LinkedIn with applicant count filtering."""
        print(f"\n🔍 Searching LinkedIn for '{keywords}' jobs...")

        # Handle multiple locations (Canada case)
        locations_to_search = []
        if isinstance(location, list):
            locations_to_search = location
            print(f"📍 Searching across {len(location)} Canadian cities")
        elif location:
            locations_to_search = [location]
            print(f"📍 Location: {location}")
        else:
            locations_to_search = [""]
            print("📍 Location: Any")

        # Show time filter info
        time_labels = {
            'r86400': '24 hours',
            'r172800': '48 hours',
            'r604800': '1 week',
            'r1209600': '2 weeks'
        }
        print(f"⏰ Time range: Last {time_labels.get(time_filter, '48 hours')}")
        print(f"👥 Looking for jobs with ≤{max_applicants} applicants")
        print("⏳ This may take a few minutes...\n")

        basic_jobs = []

        # Store experience for search filters
        self._current_experience = getattr(self, '_search_experience', None)

        # Search each location
        for search_location in locations_to_search:
            if search_location:
                print(f"\n🔍 Searching in: {search_location}")

            location_jobs = self.search_single_location(
                keywords, search_location, max_applicants, max_results // len(locations_to_search), time_filter
            )
            basic_jobs.extend(location_jobs)

            if len(basic_jobs) >= max_results:
                basic_jobs = basic_jobs[:max_results]
                break

        # Phase 2: Fetch detailed job information
        if basic_jobs:
            print(f"\n📖 Phase 2: Fetching detailed job descriptions for {len(basic_jobs)} jobs...")
            print("⏳ This will take a few minutes to get full job details...\n")

            for i, job in enumerate(basic_jobs, 1):
                print(f"📄 {i}/{len(basic_jobs)}: Getting details for {job['title']} at {job['company']}")

                detailed_job = self.get_detailed_job_info(job)
                self.results.append(detailed_job)

                # Rate limiting - be respectful
                time.sleep(random.uniform(2, 4))

        print(f"\n✅ Completed! Found {len(self.results)} jobs with detailed information.")

    def search_single_location(self, keywords, location, max_applicants, max_results_per_location, time_filter='r172800'):
        """Search for jobs in a single location with improved pagination."""
        # Try multiple LinkedIn endpoints and approaches
        search_urls = [
            "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search",
            "https://www.linkedin.com/jobs/search"
        ]

        # Search parameters with better keyword matching for more precise results
        params = {
            'keywords': keywords.replace(' ', '+'),
            'location': location,
            'start': 0,
            'count': 25,
            'f_TPR': time_filter,  # User-selected time range
            'f_JT': 'F,P,C',       # Full-time, Part-time, Contract
            'sortBy': 'R',         # Sort by relevance for better matching
        }

        # Add experience level filter if specified
        experience = getattr(self, '_current_experience', None)
        if experience is not None:
            if experience <= 1:
                params['f_E'] = '1'  # Entry level
            elif experience <= 3:
                params['f_E'] = '2'  # Associate
            elif experience <= 7:
                params['f_E'] = '3,4'  # Mid-Senior level
            else:
                params['f_E'] = '5,6'  # Director/Executive

        jobs_found = 0
        start = 0
        location_basic_jobs = []
        pages_without_results = 0
        max_pages_without_results = 2  # Reduce to avoid too many failed requests
        rate_limit_errors = 0
        max_rate_limit_errors = 3

        # Try different approaches if rate limited
        for base_url in search_urls:
            if rate_limit_errors >= max_rate_limit_errors:
                print(f"   🚫 Too many rate limit errors, trying alternative approach...")
                break

            print(f"   🔍 Trying endpoint: {base_url.split('/')[-1]}")

            current_start = start
            current_pages_without_results = 0

            while (jobs_found < max_results_per_location and
                   current_pages_without_results < max_pages_without_results and
                   rate_limit_errors < max_rate_limit_errors):

                params['start'] = current_start
                page_jobs_found = 0

                try:
                    # Add longer delay before each request to avoid rate limiting
                    time.sleep(random.uniform(3, 6))

                    response = self.session.get(base_url, params=params, timeout=20)

                    if response.status_code == 429:
                        print(f"   ⏳ Rate limited - waiting longer...")
                        rate_limit_errors += 1
                        time.sleep(random.uniform(10, 15))  # Much longer wait
                        continue

                    response.raise_for_status()

                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Try multiple selectors for job cards
                    job_cards = (soup.find_all('div', class_='job-search-card') or
                               soup.find_all('div', class_='jobs-search-results__list-item') or
                               soup.find_all('div', class_='result-card') or
                               soup.find_all('li', class_='result-card'))

                    if not job_cards:
                        print(f"   🔍 No job cards found on page {(current_start // 25) + 1}")
                        current_pages_without_results += 1
                        current_start += 25
                        continue

                    current_page = (current_start // 25) + 1
                    print(f"   📄 Processing page {current_page} - Found {len(job_cards)} job cards")

                    for card in job_cards:
                        try:
                            job_data = self.extract_linkedin_job_data(card, fetch_details=False)
                            if job_data and job_data['title'] != 'N/A':
                                # Check if job is actually relevant to search keywords
                                if self.is_job_relevant(job_data['title'], keywords):
                                    # Filter by applicant count if available
                                    applicants = job_data.get('applicants')
                                    if applicants is None or applicants <= max_applicants:
                                        location_basic_jobs.append(job_data)
                                        jobs_found += 1
                                        page_jobs_found += 1

                                        applicant_text = f"({applicants} applicants)" if applicants is not None else "(Applicants unknown)"
                                        location_text = f" | {location}" if location else ""
                                        print(f"   ✅ {jobs_found}. {job_data['title']} at {job_data['company']} {applicant_text}{location_text}")

                                        if jobs_found >= max_results_per_location:
                                            break
                                else:
                                    print(f"   🔄 Skipped irrelevant: {job_data['title']} at {job_data['company']}")
                        except Exception as e:
                            print(f"   ⚠️  Error processing job card: {e}")
                            continue

                    if page_jobs_found == 0:
                        current_pages_without_results += 1
                    else:
                        current_pages_without_results = 0  # Reset counter if we found jobs

                    current_start += 25

                except requests.exceptions.RequestException as e:
                    if "429" in str(e):
                        print(f"   ⏳ Rate limited - waiting and retrying...")
                        rate_limit_errors += 1
                        time.sleep(random.uniform(15, 25))
                        continue
                    else:
                        print(f"   ❌ Network error on page {(current_start // 25) + 1}: {e}")
                        current_pages_without_results += 1
                        if current_pages_without_results >= max_pages_without_results:
                            break
                        time.sleep(random.uniform(5, 8))
                        current_start += 25
                        continue
                except Exception as e:
                    print(f"   ❌ Unexpected error on page {(current_start // 25) + 1}: {e}")
                    current_pages_without_results += 1
                    current_start += 25
                    continue

            if jobs_found > 0:
                break  # Found some jobs, no need to try other endpoints

        location_text = f" in {location}" if location else ""
        print(f"   📊 Found {len(location_basic_jobs)} qualifying jobs{location_text}")
        return location_basic_jobs

    def search_linkedin_jobs_basic(self, keywords, location="", max_applicants=10, max_results=50, time_filter='r172800'):
        """Quick search for basic job information without detailed descriptions."""
        print(f"\n🔍 Searching LinkedIn for '{keywords}' jobs (Basic Mode)...")

        # Handle multiple locations (Canada case)
        locations_to_search = []
        if isinstance(location, list):
            locations_to_search = location
            print(f"📍 Searching across {len(location)} Canadian cities")
        elif location:
            locations_to_search = [location]
            print(f"📍 Location: {location}")
        else:
            locations_to_search = [""]
            print("📍 Location: Any")

        # Show time filter info
        time_labels = {
            'r86400': '24 hours',
            'r172800': '48 hours',
            'r604800': '1 week',
            'r1209600': '2 weeks'
        }
        print(f"⏰ Time range: Last {time_labels.get(time_filter, '48 hours')}")
        print(f"👥 Looking for jobs with ≤{max_applicants} applicants")
        print("⚡ Fast search mode - basic information only\n")

        # Search each location
        for search_location in locations_to_search:
            if search_location:
                print(f"\n🔍 Searching in: {search_location}")

            location_jobs = self.search_single_location_basic(
                keywords, search_location, max_applicants, max_results // len(locations_to_search), time_filter
            )

            if len(self.results) >= max_results:
                self.results = self.results[:max_results]
                break

        print(f"\n✅ Completed! Found {len(self.results)} jobs with basic information.")

    def search_single_location_basic(self, keywords, location, max_applicants, max_results_per_location, time_filter='r172800'):
        """Quick search for basic job info in a single location."""
        base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

        params = {
            'keywords': keywords.replace(' ', '+'),
            'location': location,
            'start': 0,
            'count': 25,
            'f_TPR': time_filter,  # User-selected time range
            'f_JT': 'F,P,C',       # Full-time, Part-time, Contract
            'sortBy': 'R',         # Sort by relevance for better matching
        }

        jobs_found = 0
        start = 0
        pages_without_results = 0
        max_pages_without_results = 3

        while jobs_found < max_results_per_location and pages_without_results < max_pages_without_results:
            params['start'] = start
            page_jobs_found = 0

            try:
                response = self.session.get(base_url, params=params, timeout=15)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='job-search-card')

                if not job_cards:
                    pages_without_results += 1
                    start += 25
                    continue

                current_page = (start // 25) + 1
                print(f"   📄 Processing page {current_page} - Found {len(job_cards)} job cards")

                for card in job_cards:
                    try:
                        job_data = self.extract_linkedin_job_data(card, fetch_details=False)
                        if job_data:
                            # Check if job is actually relevant to search keywords
                            if self.is_job_relevant(job_data['title'], keywords):
                                # Add basic job description placeholders
                                job_data['job_description'] = "Use detailed mode to get full job descriptions"
                                job_data['job_type'] = "Not fetched in basic mode"
                                job_data['seniority_level'] = "Not fetched in basic mode"
                                job_data['company_size'] = "Not fetched in basic mode"
                                job_data['industry'] = "Not fetched in basic mode"
                                job_data['skills_required'] = "Not fetched in basic mode"
                                job_data['salary_range'] = "Not fetched in basic mode"

                                # Filter by applicant count if available
                                applicants = job_data.get('applicants')
                                if applicants is None or applicants <= max_applicants:
                                    self.results.append(job_data)
                                    jobs_found += 1
                                    page_jobs_found += 1

                                    applicant_text = f"({applicants} applicants)" if applicants is not None else "(Applicants unknown)"
                                    location_text = f" | {location}" if location else ""
                                    print(f"   ✅ {jobs_found}. {job_data['title']} at {job_data['company']} {applicant_text}{location_text}")

                                    if jobs_found >= max_results_per_location:
                                        break
                            else:
                                print(f"   🔄 Skipped irrelevant: {job_data['title']} at {job_data['company']}")
                    except Exception as e:
                        print(f"   ⚠️  Error processing job card: {e}")
                        continue

                if page_jobs_found == 0:
                    pages_without_results += 1
                else:
                    pages_without_results = 0

                start += 25
                time.sleep(random.uniform(1.5, 3.0))

            except requests.exceptions.RequestException as e:
                print(f"   ❌ Network error on page {(start // 25) + 1}: {e}")
                pages_without_results += 1
                if pages_without_results >= max_pages_without_results:
                    break
                time.sleep(random.uniform(2, 4))
                start += 25
                continue
            except Exception as e:
                print(f"   ❌ Unexpected error on page {(start // 25) + 1}: {e}")
                pages_without_results += 1
                start += 25
                continue

        location_text = f" in {location}" if location else ""
        print(f"   📊 Found {jobs_found} qualifying jobs{location_text}")
        return jobs_found

    def extract_linkedin_job_data(self, job_card, fetch_details=True):
        """Extract job data from LinkedIn job card."""
        try:
            # Extract basic job information
            title_elem = job_card.find('h3', class_='base-search-card__title')
            title = title_elem.get_text(strip=True) if title_elem else "N/A"

            company_elem = job_card.find('h4', class_='base-search-card__subtitle')
            company = company_elem.get_text(strip=True) if company_elem else "N/A"

            location_elem = job_card.find('span', class_='job-search-card__location')
            location = location_elem.get_text(strip=True) if location_elem else "N/A"

            link_elem = job_card.find('a', class_='base-card__full-link')
            job_link = link_elem.get('href') if link_elem else "N/A"

            # Try to extract posting date
            date_elem = job_card.find('time', class_='job-search-card__listdate')
            posting_date = date_elem.get('datetime') if date_elem else "N/A"

            # Extract job ID for detailed information
            job_id = None
            if job_link and 'linkedin.com/jobs/view/' in job_link:
                # Extract numeric job ID from URL like https://www.linkedin.com/jobs/view/1234567890/
                import re
                job_id_match = re.search(r'/jobs/view/(\d+)', job_link)
                if job_id_match:
                    job_id = job_id_match.group(1)

            # Get basic applicant count quickly if requested
            applicants = None
            if fetch_details and job_id:
                applicants = self.get_linkedin_applicant_count(job_id)

            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'link': job_link,
                'job_id': job_id,
                'applicants': applicants,
                'posting_date': posting_date,
                'source': 'LinkedIn',
                'scraped_at': datetime.now().isoformat()
            }

            # Add placeholders for detailed info (to be filled later)
            if not fetch_details:
                job_data.update({
                    'job_description': None,
                    'job_type': None,
                    'seniority_level': None,
                    'company_size': None,
                    'industry': None,
                    'skills_required': None,
                    'salary_range': None
                })

            return job_data

        except Exception as e:
            print(f"❌ Error extracting job data: {e}")
            return None

    def get_detailed_job_info(self, basic_job):
        """Fetch detailed job information including description from the job link."""
        detailed_job = basic_job.copy()

        if not basic_job.get('link'):
            print(f"   ⚠️  No job link available for {basic_job['title']}")
            return detailed_job

        try:
            # Method 1: Try the direct LinkedIn job page URL
            job_url = basic_job['link']

            # Clean up the URL - remove tracking parameters
            if '?' in job_url:
                job_url = job_url.split('?')[0]

            # Ensure we have the full URL
            if not job_url.startswith('http'):
                job_url = 'https://www.linkedin.com' + job_url

            print(f"   🔗 Fetching: {job_url}")

            # First try: Direct page scraping
            response = self.session.get(job_url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract job description
            description = self.extract_job_description(soup)
            detailed_job['job_description'] = description

            # Extract additional details
            job_details = self.extract_job_details(soup)
            detailed_job.update(job_details)

            # Get applicant count if not already fetched
            if detailed_job['applicants'] is None:
                detailed_job['applicants'] = self.get_linkedin_applicant_count_from_soup(soup)

            print(f"   ✅ Got full details for {basic_job['title']}")

        except requests.exceptions.RequestException as e:
            print(f"   ❌ Network error getting details for {basic_job['title']}: {e}")
            # Try alternative approach with API endpoint if job_id is available
            if basic_job.get('job_id'):
                try:
                    api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{basic_job['job_id']}"
                    print(f"   🔄 Trying API endpoint: {api_url}")

                    response = self.session.get(api_url, timeout=15)
                    response.raise_for_status()

                    # Parse JSON response if it's JSON
                    if 'application/json' in response.headers.get('content-type', ''):
                        import json
                        job_data = json.loads(response.text)
                        # Extract description from JSON
                        if 'description' in job_data:
                            detailed_job['job_description'] = job_data['description']['text']
                        print(f"   ✅ Got details via API for {basic_job['title']}")
                    else:
                        # Parse as HTML
                        soup = BeautifulSoup(response.content, 'html.parser')
                        description = self.extract_job_description(soup)
                        detailed_job['job_description'] = description
                        print(f"   ✅ Got details via API (HTML) for {basic_job['title']}")

                except Exception as api_error:
                    print(f"   ❌ API fallback also failed: {api_error}")
                    detailed_job['job_description'] = "Could not fetch job description"
            else:
                detailed_job['job_description'] = "Could not fetch job description"

        except Exception as e:
            print(f"   ❌ Error getting details for {basic_job['title']}: {e}")
            detailed_job['job_description'] = "Could not fetch job description"

        return detailed_job

    def extract_job_description(self, soup):
        """Extract the job description from LinkedIn job page."""
        # Updated selectors based on current LinkedIn structure
        description_selectors = [
            # Primary selectors for job description
            'div.show-more-less-html__markup',
            'div.jobs-description__content',
            'div.description__text',
            'section.jobs-description',
            'div.jobs-box__html-content',
            'div.jobs-description-content__text',

            # Alternative selectors
            '[data-section="description"]',
            'div[class*="description"]',
            'section[class*="description"]',
            '.jobs-description',
            '.job-description',

            # Generic content selectors
            'div.job-view-layout',
            'article',
            'main'
        ]

        for selector in description_selectors:
            try:
                # Use CSS selector for more flexible matching
                elements = soup.select(selector)

                for elem in elements:
                    if elem:
                        # Clean up the description text
                        description = elem.get_text(separator='\n', strip=True)
                        if description and len(description) > 100:  # Ensure it's substantial
                            # Clean up extra whitespace and format nicely
                            lines = [line.strip() for line in description.split('\n') if line.strip()]
                            clean_description = '\n'.join(lines)

                            # Filter out navigation/header text
                            if len(clean_description) > 200 and not clean_description.lower().startswith(('sign in', 'linkedin', 'home')):
                                return clean_description
            except Exception:
                continue

        # Fallback 1: Look for specific patterns in the text
        try:
            # Look for sections that contain job-related keywords
            job_keywords = ['responsibilities', 'requirements', 'qualifications', 'experience', 'skills', 'role', 'position']

            all_text = soup.get_text()
            paragraphs = [p.strip() for p in all_text.split('\n') if len(p.strip()) > 30]

            job_related_paragraphs = []
            for para in paragraphs:
                if any(keyword in para.lower() for keyword in job_keywords):
                    job_related_paragraphs.append(para)
                    # Add context paragraphs
                    para_index = paragraphs.index(para)
                    for i in range(max(0, para_index-2), min(len(paragraphs), para_index+3)):
                        if paragraphs[i] not in job_related_paragraphs:
                            job_related_paragraphs.append(paragraphs[i])

            if job_related_paragraphs:
                return '\n'.join(job_related_paragraphs[:15])  # First 15 relevant paragraphs
        except Exception:
            pass

        # Fallback 2: Extract substantial text blocks
        try:
            text_content = soup.get_text()
            if len(text_content) > 500:
                # Try to extract what looks like a job description
                paragraphs = [p.strip() for p in text_content.split('\n') if len(p.strip()) > 50]
                if paragraphs:
                    # Filter out likely navigation/header content
                    filtered_paragraphs = []
                    skip_phrases = ['sign in', 'linkedin', 'home', 'jobs', 'messaging', 'notifications']

                    for para in paragraphs[:20]:  # Check first 20 paragraphs
                        if not any(phrase in para.lower() for phrase in skip_phrases):
                            filtered_paragraphs.append(para)

                    if filtered_paragraphs:
                        return '\n'.join(filtered_paragraphs[:10])
        except Exception:
            pass

        return "Job description not available"

    def extract_job_details(self, soup):
        """Extract additional job details like job type, seniority, etc."""
        details = {
            'job_type': None,
            'seniority_level': None,
            'company_size': None,
            'industry': None,
            'skills_required': None,
            'salary_range': None
        }

        # Extract job type (Full-time, Part-time, etc.)
        job_type_elem = soup.find(string=re.compile(r'(Full-time|Part-time|Contract|Temporary|Internship)', re.I))
        if job_type_elem:
            details['job_type'] = job_type_elem.strip()

        # Extract seniority level
        seniority_elem = soup.find(string=re.compile(r'(Entry level|Associate|Mid-Senior level|Director|Executive)', re.I))
        if seniority_elem:
            details['seniority_level'] = seniority_elem.strip()

        # Extract skills (look for skills section)
        skills_section = soup.find('section', class_=lambda x: x and 'skill' in x.lower())
        if skills_section:
            skills = [skill.get_text(strip=True) for skill in skills_section.find_all(['span', 'div']) if skill.get_text(strip=True)]
            if skills:
                details['skills_required'] = ', '.join(skills[:10])  # First 10 skills

        # Extract salary information
        salary_elem = soup.find(string=re.compile(r'\$\d+', re.I))
        if salary_elem:
            # Look for salary patterns
            salary_match = re.search(r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?(?:\s*(?:per|/)\s*(?:year|hour|month))?', salary_elem)
            if salary_match:
                details['salary_range'] = salary_match.group(0)

        # Extract industry
        industry_elem = soup.find(string=re.compile(r'(Technology|Healthcare|Finance|Education|Manufacturing)', re.I))
        if industry_elem:
            details['industry'] = industry_elem.strip()

        return details

    def get_linkedin_applicant_count_from_soup(self, soup):
        """Extract applicant count from already fetched soup."""
        applicant_patterns = [
            r'(\d+)\s+applicants?',
            r'be\s+among\s+the\s+first\s+(\d+)\s+applicants?',
            r'over\s+(\d+)\s+applicants?',
            r'(\d+)\s+people\s+applied',
        ]

        page_text = soup.get_text().lower()

        for pattern in applicant_patterns:
            matches = re.findall(pattern, page_text)
            if matches:
                return int(matches[0])

        # If no specific number found, look for qualitative indicators
        if 'be among the first' in page_text and 'applicant' in page_text:
            return 5  # Estimate low applicant count

        return None

    def get_linkedin_applicant_count(self, job_id):
        """Get applicant count for a specific LinkedIn job."""
        if not job_id:
            return None

        try:
            detail_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
            response = self.session.get(detail_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Look for applicant count indicators in various formats
            applicant_patterns = [
                r'(\d+)\s+applicants?',
                r'be\s+among\s+the\s+first\s+(\d+)\s+applicants?',
                r'over\s+(\d+)\s+applicants?',
                r'(\d+)\s+people\s+applied',
            ]

            page_text = soup.get_text().lower()

            for pattern in applicant_patterns:
                matches = re.findall(pattern, page_text)
                if matches:
                    return int(matches[0])

            # If no specific number found, look for qualitative indicators
            if 'be among the first' in page_text and 'applicant' in page_text:
                # Estimate low applicant count
                return 5

            time.sleep(random.uniform(0.5, 1))  # Rate limiting
            return None

        except Exception as e:
            return None

    def create_output_directory(self, job_title):
        """Create organized output directory structure."""
        # Sanitize job title for filename
        safe_job_title = re.sub(r'[^\w\s-]', '', job_title).strip()
        safe_job_title = re.sub(r'[-\s]+', '_', safe_job_title).lower()

        # Create directory structure: job_search_output/YYYY-MM-DD/
        today = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path(__file__).parent.parent / "job_search_output" / today
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%H%M%S")
        csv_filename = f"{safe_job_title}_{timestamp}.csv"
        json_filename = f"{safe_job_title}_{timestamp}.json"

        return {
            'csv': output_dir / csv_filename,
            'json': output_dir / json_filename
        }

    def save_results(self, filepaths, search_params):
        """Save search results to both CSV and JSON files with metadata."""
        if not self.results:
            print("❌ No results to save.")
            return False

        success = True

        # Save CSV file
        try:
            with open(filepaths['csv'], 'w', newline='', encoding='utf-8') as csvfile:
                # Write metadata as comments at the top
                csvfile.write(f"# Job Search Results\n")
                csvfile.write(f"# Search Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                csvfile.write(f"# Job Title: {search_params['job_title']}\n")
                csvfile.write(f"# Experience: {search_params['experience'] or 'Any'} years\n")
                csvfile.write(f"# Location: {search_params['location'] or 'Any'}\n")
                csvfile.write(f"# Max Applicants: {search_params['max_applicants']}\n")
                csvfile.write(f"# Total Results: {len(self.results)}\n")
                csvfile.write(f"#\n")

                # Write CSV headers and data
                fieldnames = [
                    'title', 'company', 'location', 'link', 'job_id', 'applicants',
                    'posting_date', 'job_description', 'job_type', 'seniority_level',
                    'company_size', 'industry', 'skills_required', 'salary_range',
                    'source', 'scraped_at'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for job in self.results:
                    writer.writerow(job)

            print(f"✅ CSV results saved to: {filepaths['csv']}")

        except Exception as e:
            print(f"❌ Error saving CSV results: {e}")
            success = False

        # Save JSON file
        try:
            json_data = {
                'metadata': {
                    'search_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'job_title': search_params['job_title'],
                    'experience': search_params['experience'] or 'Any',
                    'location': search_params['location'] or 'Any',
                    'max_applicants': search_params['max_applicants'],
                    'total_results': len(self.results),
                    'search_mode': 'Detailed' if search_params.get('fetch_details') else 'Basic'
                },
                'jobs': self.results
            }

            with open(filepaths['json'], 'w', encoding='utf-8') as jsonfile:
                json.dump(json_data, jsonfile, indent=2, ensure_ascii=False, default=str)

            print(f"✅ JSON results saved to: {filepaths['json']}")

        except Exception as e:
            print(f"❌ Error saving JSON results: {e}")
            success = False

        return success

    def display_summary(self, filepaths, search_params):
        """Display search summary and results location."""
        print("\n" + "=" * 60)
        print("🎯 SEARCH COMPLETED!")
        print("=" * 60)
        print(f"📋 Job Title: {search_params['job_title']}")
        print(f"💼 Experience: {search_params['experience'] or 'Any'} years")
        print(f"📍 Location: {search_params['location'] or 'Any'}")
        print(f"👥 Max Applicants: {search_params['max_applicants']}")
        print(f"🔍 Jobs Found: {len(self.results)}")
        print(f"💾 CSV results: {filepaths['csv']}")
        print(f"📄 JSON results: {filepaths['json']}")
        print("=" * 60)

        if self.results:
            print("\n📊 TOP 5 RESULTS WITH DETAILS:")
            print("-" * 80)
            for i, job in enumerate(self.results[:5], 1):
                applicants_text = f"({job['applicants']} applicants)" if job['applicants'] is not None else "(Unknown applicants)"
                job_type_text = f" | {job['job_type']}" if job['job_type'] else ""
                seniority_text = f" | {job['seniority_level']}" if job['seniority_level'] else ""
                salary_text = f" | {job['salary_range']}" if job['salary_range'] else ""

                print(f"{i}. {job['title']}")
                print(f"   🏢 {job['company']}")
                print(f"   📍 {job['location']}")
                print(f"   👥 {applicants_text}{job_type_text}{seniority_text}{salary_text}")

                # Show truncated job description
                if job.get('job_description') and job['job_description'] != "Job description not available":
                    description = job['job_description']
                    if len(description) > 200:
                        description = description[:200] + "..."
                    print(f"   📝 {description}")

                # Show skills if available
                if job.get('skills_required'):
                    skills = job['skills_required']
                    if len(skills) > 100:
                        skills = skills[:100] + "..."
                    print(f"   🛠️  Skills: {skills}")

                print(f"   🔗 {job['link']}")
                print()

def main():
    """Main function to run the interactive job search."""
    try:
        searcher = InteractiveJobSearcher()

        # Get user input
        search_params = searcher.get_user_input()

        # Create search keywords
        keywords = searcher.create_search_keywords(
            search_params['job_title'],
            search_params['experience']
        )

        print(f"\n🔍 Search Keywords: '{keywords}'")

        # Confirm search
        confirm = input("\n▶️  Start search? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Search cancelled.")
            return

        # Store experience for search filters
        searcher._search_experience = search_params['experience']

        # Perform search
        if search_params['fetch_details']:
            searcher.search_linkedin_jobs(
                keywords=keywords,
                location=search_params['location'],
                max_applicants=search_params['max_applicants'],
                max_results=search_params['max_results'],
                time_filter=search_params['time_filter']
            )
        else:
            # Quick search without detailed descriptions
            searcher.search_linkedin_jobs_basic(
                keywords=keywords,
                location=search_params['location'],
                max_applicants=search_params['max_applicants'],
                max_results=search_params['max_results'],
                time_filter=search_params['time_filter']
            )

        if searcher.results:
            # Create output directory and save results
            output_files = searcher.create_output_directory(search_params['job_title'])

            if searcher.save_results(output_files, search_params):
                searcher.display_summary(output_files, search_params)
            else:
                print("❌ Failed to save results.")
        else:
            print("\n❌ No jobs found matching your criteria.")
            print("💡 Try:")
            print("   - Broadening your search terms")
            print("   - Increasing max applicants")
            print("   - Changing location")
            print("   - Adjusting experience level")

    except KeyboardInterrupt:
        print("\n\n❌ Search interrupted by user.")
        if searcher.results:
            print(f"📊 Found {len(searcher.results)} jobs before interruption.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()