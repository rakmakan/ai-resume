#!/usr/bin/env python3
"""
Resume AI Creator Script

This script uses Claude AI to tailor resume sections based on job descriptions.
It reads job details from a resume folder and uses the job_prompt.jinja template
to generate tailored resume content via Claude SDK in headless mode.

Usage:
    python resume_ai_creator.py --path /path/to/resume/folder

Example:
    python resume_ai_creator.py --path "/Users/rakshitmakan/Documents/Resume/resumes/Senior Agent AI engineer/jobgether"
"""

import argparse
import json
import os
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Optional

import jinja2


def load_job_details(resume_path: Path) -> Dict:
    """Load job details from job_details.json in the resume folder."""
    job_details_file = resume_path / "job_details.json"

    if not job_details_file.exists():
        raise FileNotFoundError(f"job_details.json not found in {resume_path}")

    with open(job_details_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_jinja_template(template_path: Path) -> jinja2.Template:
    """Load and return the Jinja2 template."""
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    env = jinja2.Environment(
        loader=jinja2.BaseLoader(),
        trim_blocks=True,
        lstrip_blocks=True
    )
    return env.from_string(template_content)


def get_section_paths(resume_path: Path) -> Dict[str, Path]:
    """Get paths to all resume section files."""
    sections_dir = resume_path / "sections"

    if not sections_dir.exists():
        raise FileNotFoundError(f"Sections directory not found: {sections_dir}")

    section_files = {
        'experience_tex_path': sections_dir / "experience.tex",
        'skills_tex_path': sections_dir / "skills.tex",
        'projects_tex_path': sections_dir / "projects.tex",
        'header_tex_path': sections_dir / "header.tex",
        'education_tex_path': sections_dir / "education.tex"
    }

    # Check which files exist
    existing_files = {}
    for key, path in section_files.items():
        if path.exists():
            existing_files[key] = str(path)
        else:
            print(f"Warning: {path} not found, skipping...")

    return existing_files


def render_prompt(template: jinja2.Template, job_details: Dict, section_paths: Dict[str, str], resume_path: Path) -> str:
    """Render the Jinja2 template with job details and section paths."""
    template_vars = {
        'company_name': job_details.get('company_name', 'Unknown Company'),
        'job_title': job_details.get('job_title', 'Unknown Position'),
        'job_description': job_details.get('job_description', ''),
        'section_path': str(resume_path / "sections"),
        'resume_tex_path': str(resume_path / "resume.tex"),
        **section_paths
    }

    return template.render(**template_vars)


def call_claude_headless(prompt: str, resume_path: Path) -> str:
    """Call Claude SDK in headless mode with the rendered prompt."""
    print("🤖 Calling Claude AI to tailor resume sections...")

    # Create temporary file for the prompt
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(prompt)
        temp_prompt_path = temp_file.name

    try:
        # Claude command with specific tools and verbose output
        cmd = [
            'claude',
            '-p', prompt,
            '--output-format', 'stream-json',
            '--verbose',
            '--allowedTools', 'Read,Edit,Write',
            '--permission-mode', 'acceptEdits'
        ]

        print(f"📂 Working directory: {resume_path}")
        print("⚡ Running Claude AI with real-time output...")
        print("-" * 80)

        # Execute Claude command from the resume directory with real-time output
        process = subprocess.Popen(
            cmd,
            cwd=str(resume_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # Stream output in real-time
        output_lines = []
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                output_lines.append(output)

        # Wait for process to complete
        return_code = process.poll()
        full_output = ''.join(output_lines)

        if return_code != 0:
            raise RuntimeError(f"Claude command failed with return code {return_code}")

        return full_output

    finally:
        # Clean up temporary file
        os.unlink(temp_prompt_path)


def parse_claude_response(response: str) -> Dict:
    """Parse Claude's JSON response."""
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse Claude response as JSON: {e}")
        return {"raw_response": response}


def main():
    """Main function to run the resume AI creator."""
    parser = argparse.ArgumentParser(
        description="Create tailored resume sections using Claude AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python resume_ai_creator.py --path "/Users/rakshitmakan/Documents/Resume/resumes/Senior Agent AI engineer/jobgether"
  python resume_ai_creator.py --path "resumes/software engineer/meta"
        """
    )

    parser.add_argument(
        '--path',
        type=str,
        required=True,
        help='Path to the resume folder containing job_details.json and sections/'
    )

    parser.add_argument(
        '--template',
        type=str,
        default='job_prompt.jinja',
        help='Path to the Jinja2 template file (default: job_prompt.jinja)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show the rendered prompt without calling Claude'
    )

    args = parser.parse_args()

    # Convert paths to Path objects
    resume_path = Path(args.path).resolve()
    template_path = Path(args.template).resolve()

    print(f"📁 Resume folder: {resume_path}")
    print(f"📄 Template: {template_path}")

    try:
        # Validate resume folder
        if not resume_path.exists():
            raise FileNotFoundError(f"Resume folder not found: {resume_path}")

        if not resume_path.is_dir():
            raise ValueError(f"Path is not a directory: {resume_path}")

        # Load job details
        print("📋 Loading job details...")
        job_details = load_job_details(resume_path)
        print(f"🏢 Company: {job_details.get('company_name')}")
        print(f"💼 Position: {job_details.get('job_title')}")

        # Load template
        print("📝 Loading Jinja2 template...")
        template = load_jinja_template(template_path)

        # Get section paths
        print("📂 Finding resume section files...")
        section_paths = get_section_paths(resume_path)
        print(f"✅ Found {len(section_paths)} section files")

        # Render prompt
        print("🔧 Rendering prompt with job details...")
        rendered_prompt = render_prompt(template, job_details, section_paths, resume_path)

        if args.dry_run:
            print("\n" + "="*80)
            print("RENDERED PROMPT (DRY RUN)")
            print("="*80)
            print(rendered_prompt)
            print("="*80)
            return

        # Call Claude
        claude_response = call_claude_headless(rendered_prompt, resume_path)

        # Parse and display response
        parsed_response = parse_claude_response(claude_response)

        print("\n✅ Claude AI processing completed!")
        print(f"📊 Response length: {len(claude_response)} characters")

        # Save response for debugging
        response_file = resume_path / "claude_response.json"
        with open(response_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_response, f, indent=2, ensure_ascii=False)

        print(f"💾 Full response saved to: {response_file}")
        print("\n🎯 Resume sections have been tailored for this job application!")

    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()