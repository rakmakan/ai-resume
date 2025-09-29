#!/usr/bin/env python3
"""
AI Resume Workflow Orchestrator

This script orchestrates the end-to-end resume creation workflow:
1. Job Search
2. Folder Creation
3. AI Tailoring
4. PDF Build

Usage:
    python run_workflow.py --config data_scientist_remote
    python run_workflow.py --config ml_engineer_toronto --resume-from step3
    python run_workflow.py --list-configs
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class WorkflowOrchestrator:
    """Orchestrates the end-to-end resume creation workflow."""

    def __init__(self, config_name: str, config_file: str = "workflow_config.yaml"):
        self.config_name = config_name
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.state = self._load_state()
        self.logger = self._setup_logging()
        self.script_dir = Path(__file__).parent.resolve()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

        with open(self.config_file, 'r') as f:
            all_configs = yaml.safe_load(f)

        if self.config_name not in all_configs.get('configs', {}):
            available = ', '.join(all_configs.get('configs', {}).keys())
            raise ValueError(
                f"Config '{self.config_name}' not found. "
                f"Available configs: {available}"
            )

        config = all_configs['configs'][self.config_name]
        defaults = all_configs.get('defaults', {})

        # Merge with defaults
        return self._merge_with_defaults(config, defaults)

    def _merge_with_defaults(self, config: Dict, defaults: Dict) -> Dict:
        """Merge config with default values."""
        for key, value in defaults.items():
            if key not in config:
                config[key] = value
            elif isinstance(value, dict) and isinstance(config[key], dict):
                config[key] = self._merge_with_defaults(config[key], value)
        return config

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO'))

        logger = logging.getLogger('WorkflowOrchestrator')
        logger.setLevel(level)
        logger.handlers.clear()

        # Console handler
        if log_config.get('console', True):
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

        # File handler
        if 'file' in log_config:
            log_file = log_config['file'].format(
                timestamp=datetime.now().strftime('%Y%m%d_%H%M%S')
            )
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        return logger

    def _load_state(self) -> Dict[str, Any]:
        """Load workflow state for resumption."""
        workflow_config = self.config.get('workflow', {})
        if not workflow_config.get('save_state', True):
            return {'completed_steps': [], 'data': {}}

        state_file = Path(workflow_config.get('state_file', '.workflow_state.json'))
        if state_file.exists():
            with open(state_file, 'r') as f:
                return json.load(f)

        return {'completed_steps': [], 'data': {}}

    def _save_state(self):
        """Save workflow state."""
        workflow_config = self.config.get('workflow', {})
        if not workflow_config.get('save_state', True):
            return

        state_file = Path(workflow_config.get('state_file', '.workflow_state.json'))
        with open(state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def _confirm(self, message: str, default: bool = True) -> bool:
        """Ask user for confirmation."""
        choices = '[Y/n]' if default else '[y/N]'
        while True:
            response = input(f"\n{message} {choices}: ").strip().lower()
            if response == '':
                return default
            if response in ['y', 'yes']:
                return True
            if response in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'")

    def _should_confirm(self, step: str) -> bool:
        """Check if confirmation is required for this step."""
        confirmations = self.config.get('workflow', {}).get('confirmations', {})
        return confirmations.get(step, True)

    def _run_command(
        self,
        cmd: List[str],
        cwd: Optional[Path] = None,
        capture_output: bool = False
    ) -> subprocess.CompletedProcess:
        """Run a shell command."""
        self.logger.debug(f"Running command: {' '.join(cmd)}")
        cwd = cwd or self.script_dir

        if capture_output:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(cmd, cwd=cwd)

        if result.returncode != 0:
            error_msg = f"Command failed with return code {result.returncode}"
            if capture_output and result.stderr:
                error_msg += f"\nError: {result.stderr}"
            raise RuntimeError(error_msg)

        return result

    def step1_job_search(self) -> Optional[Path]:
        """Step 1: Search for jobs."""
        if 'step1_job_search' in self.state['completed_steps']:
            self.logger.info("⏭️  Step 1 (Job Search) already completed, skipping...")
            return Path(self.state['data'].get('job_search_output'))

        config = self.config.get('job_search', {})
        if not config.get('enabled', True):
            self.logger.info("⏭️  Step 1 (Job Search) disabled, skipping...")
            return None

        self.logger.info("=" * 80)
        self.logger.info("📋 STEP 1: JOB SEARCH")
        self.logger.info("=" * 80)
        self.logger.info(f"Job Title: {config.get('title')}")
        self.logger.info(f"Location: {config.get('location')}")
        self.logger.info(f"Results: {config.get('num_results')}")

        # Build command
        script_path = self.script_dir / config.get('script_path', 'fetch_job/job_search.py')

        # Determine command based on script type
        if script_path.suffix == '.sh':
            cmd = ['bash', str(script_path)]
        else:
            cmd = ['python3', str(script_path)]

        # Add arguments
        cmd.extend([
            '--title', config.get('title'),
            '--location', config.get('location', 'Remote'),
            '--num-results', str(config.get('num_results', 10))
        ])

        # Add filters if present
        filters = config.get('filters', {})
        if filters:
            self.logger.info(f"Filters: {filters}")

        # Run job search
        self.logger.info("\n🔍 Running job search...")
        result = self._run_command(cmd, capture_output=True)

        # Find the most recent output file
        output_dir = self.script_dir / config.get('output_dir', 'job_search_output')
        if not output_dir.exists():
            raise RuntimeError(f"Job search output directory not found: {output_dir}")

        # Get most recent JSON file
        json_files = sorted(output_dir.rglob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
        if not json_files:
            raise RuntimeError("No job search output files found")

        output_file = json_files[0]
        self.logger.info(f"✅ Job search completed: {output_file}")

        # Save state
        self.state['completed_steps'].append('step1_job_search')
        self.state['data']['job_search_output'] = str(output_file)
        self._save_state()

        # Confirmation
        if self._should_confirm('after_search'):
            # Show summary
            with open(output_file, 'r') as f:
                data = json.load(f)
                num_jobs = len(data.get('jobs', []))
                self.logger.info(f"\n📊 Found {num_jobs} jobs")

            if not self._confirm("Continue to next step (Folder Creation)?"):
                self.logger.info("⏸️  Workflow paused. Resume with: python run_workflow.py --config {self.config_name} --resume")
                sys.exit(0)

        return output_file

    def step2_folder_creation(self, job_search_output: Path) -> List[Path]:
        """Step 2: Create resume folders for selected jobs."""
        if 'step2_folder_creation' in self.state['completed_steps']:
            self.logger.info("⏭️  Step 2 (Folder Creation) already completed, skipping...")
            return [Path(p) for p in self.state['data'].get('created_folders', [])]

        config = self.config.get('folder_creation', {})
        if not config.get('enabled', True):
            self.logger.info("⏭️  Step 2 (Folder Creation) disabled, skipping...")
            return []

        self.logger.info("\n" + "=" * 80)
        self.logger.info("📁 STEP 2: FOLDER CREATION")
        self.logger.info("=" * 80)

        script_path = self.script_dir / config.get('script_path', 'create_job_folder.sh')
        selection_mode = config.get('selection_mode', 'manual')

        self.logger.info(f"Selection mode: {selection_mode}")
        self.logger.info(f"Job search output: {job_search_output}")

        # Build command
        cmd = [
            'bash',
            str(script_path),
            '--json_path', str(job_search_output)
        ]

        # Run folder creation
        self.logger.info("\n📂 Creating resume folders...")
        self.logger.info("(You will be prompted to select jobs)")

        self._run_command(cmd)

        # Find created folders
        with open(job_search_output, 'r') as f:
            data = json.load(f)
            job_title = data['metadata']['job_title']

        resume_base = self.script_dir / config.get('output_base', 'resumes')
        title_dir = resume_base / job_title

        if not title_dir.exists():
            self.logger.warning("No folders created")
            return []

        # Get folders created in the last minute
        import time
        cutoff_time = time.time() - 60
        created_folders = [
            d for d in title_dir.iterdir()
            if d.is_dir() and d.stat().st_mtime > cutoff_time
        ]

        self.logger.info(f"✅ Created {len(created_folders)} resume folders")
        for folder in created_folders:
            self.logger.info(f"   - {folder.name}")

        # Save state
        self.state['completed_steps'].append('step2_folder_creation')
        self.state['data']['created_folders'] = [str(f) for f in created_folders]
        self.state['data']['job_title'] = job_title
        self._save_state()

        # Confirmation
        if self._should_confirm('after_folder_creation'):
            if not self._confirm("Continue to next step (AI Tailoring)?"):
                self.logger.info("⏸️  Workflow paused. Resume with: python run_workflow.py --config {self.config_name} --resume")
                sys.exit(0)

        return created_folders

    def step3_ai_tailoring(self, resume_folders: List[Path]):
        """Step 3: AI-powered resume tailoring."""
        if 'step3_ai_tailoring' in self.state['completed_steps']:
            self.logger.info("⏭️  Step 3 (AI Tailoring) already completed, skipping...")
            return

        config = self.config.get('ai_tailoring', {})
        if not config.get('enabled', True):
            self.logger.info("⏭️  Step 3 (AI Tailoring) disabled, skipping...")
            return

        self.logger.info("\n" + "=" * 80)
        self.logger.info("🤖 STEP 3: AI RESUME TAILORING")
        self.logger.info("=" * 80)

        script_path = self.script_dir / config.get('script_path', 'resume_ai_creator.py')
        process_mode = config.get('process_mode', 'sequential')

        self.logger.info(f"Processing {len(resume_folders)} resumes in {process_mode} mode")

        for i, folder in enumerate(resume_folders, 1):
            self.logger.info(f"\n[{i}/{len(resume_folders)}] Processing: {folder.name}")

            # Build command
            cmd = [
                'python3',
                str(script_path),
                '--path', str(folder)
            ]

            if config.get('prompt_template'):
                cmd.extend(['--template', config['prompt_template']])

            try:
                self.logger.info("🔄 Running AI tailoring...")
                self._run_command(cmd)
                self.logger.info(f"✅ Tailoring completed for {folder.name}")
            except Exception as e:
                self.logger.error(f"❌ Tailoring failed for {folder.name}: {e}")
                if not self.config.get('workflow', {}).get('continue_on_error', False):
                    raise

        # Save state
        self.state['completed_steps'].append('step3_ai_tailoring')
        self._save_state()

        # Confirmation
        if self._should_confirm('after_tailoring'):
            if not self._confirm("Continue to next step (Build PDFs)?"):
                self.logger.info("⏸️  Workflow paused. Resume with: python run_workflow.py --config {self.config_name} --resume")
                sys.exit(0)

    def step4_build_pdfs(self, resume_folders: List[Path]):
        """Step 4: Build PDF resumes."""
        if 'step4_build_pdfs' in self.state['completed_steps']:
            self.logger.info("⏭️  Step 4 (Build PDFs) already completed, skipping...")
            return

        config = self.config.get('build', {})
        if not config.get('enabled', True):
            self.logger.info("⏭️  Step 4 (Build PDFs) disabled, skipping...")
            return

        self.logger.info("\n" + "=" * 80)
        self.logger.info("📄 STEP 4: BUILD PDF RESUMES")
        self.logger.info("=" * 80)

        script_path = self.script_dir / config.get('script_path', 'build.sh')
        job_title = self.state['data'].get('job_title')

        self.logger.info(f"Building PDFs for {len(resume_folders)} resumes")

        for i, folder in enumerate(resume_folders, 1):
            self.logger.info(f"\n[{i}/{len(resume_folders)}] Building: {folder.name}")

            # Build command
            cmd = [
                'bash',
                str(script_path),
                '--title', job_title,
                '--path', folder.name
            ]

            try:
                self.logger.info("🔨 Compiling LaTeX...")
                self._run_command(cmd)
                pdf_path = folder / 'resume.pdf'
                if pdf_path.exists():
                    self.logger.info(f"✅ PDF created: {pdf_path}")
                else:
                    self.logger.warning(f"⚠️  PDF not found at expected location: {pdf_path}")
            except Exception as e:
                self.logger.error(f"❌ Build failed for {folder.name}: {e}")
                if not self.config.get('workflow', {}).get('continue_on_error', False):
                    raise

        # Save state
        self.state['completed_steps'].append('step4_build_pdfs')
        self._save_state()

        # Final confirmation
        if self._should_confirm('after_build'):
            self.logger.info("\n" + "=" * 80)
            self.logger.info("🎉 WORKFLOW COMPLETED!")
            self.logger.info("=" * 80)
            self.logger.info(f"✅ Processed {len(resume_folders)} resumes")
            self.logger.info("\n📂 Resume locations:")
            for folder in resume_folders:
                pdf_path = folder / 'resume.pdf'
                if pdf_path.exists():
                    self.logger.info(f"   - {pdf_path}")

    def run(self, resume_from: Optional[str] = None):
        """Run the complete workflow."""
        self.logger.info("🚀 Starting AI Resume Workflow")
        self.logger.info(f"Configuration: {self.config_name}")
        self.logger.info(f"Description: {self.config.get('description', 'N/A')}")

        try:
            # Step 1: Job Search
            if not resume_from or resume_from in ['step1', 'beginning']:
                job_search_output = self.step1_job_search()
            else:
                job_search_output = Path(self.state['data'].get('job_search_output'))

            if not job_search_output:
                self.logger.error("❌ No job search output available")
                return

            # Step 2: Folder Creation
            if not resume_from or resume_from in ['step1', 'step2', 'beginning']:
                resume_folders = self.step2_folder_creation(job_search_output)
            else:
                resume_folders = [Path(p) for p in self.state['data'].get('created_folders', [])]

            if not resume_folders:
                self.logger.warning("⚠️  No resume folders created")
                return

            # Step 3: AI Tailoring
            if not resume_from or resume_from in ['step1', 'step2', 'step3', 'beginning']:
                self.step3_ai_tailoring(resume_folders)

            # Step 4: Build PDFs
            if not resume_from or resume_from in ['step1', 'step2', 'step3', 'step4', 'beginning']:
                self.step4_build_pdfs(resume_folders)

            self.logger.info("\n✨ All done! Your tailored resumes are ready.")

        except KeyboardInterrupt:
            self.logger.info("\n⏹️  Workflow interrupted by user")
            self.logger.info(f"Resume with: python run_workflow.py --config {self.config_name} --resume")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"\n❌ Workflow failed: {e}")
            if self.logger.level == logging.DEBUG:
                import traceback
                traceback.print_exc()
            sys.exit(1)


def list_configs(config_file: str = "workflow_config.yaml"):
    """List all available configurations."""
    config_path = Path(config_file)
    if not config_path.exists():
        print(f"❌ Config file not found: {config_file}")
        sys.exit(1)

    with open(config_path, 'r') as f:
        all_configs = yaml.safe_load(f)

    configs = all_configs.get('configs', {})
    print("\n📋 Available Configurations:")
    print("=" * 80)
    for name, config in configs.items():
        print(f"\n🔹 {name}")
        print(f"   Name: {config.get('name', 'N/A')}")
        print(f"   Description: {config.get('description', 'N/A')}")
        job_search = config.get('job_search', {})
        if job_search:
            print(f"   Job Title: {job_search.get('title', 'N/A')}")
            print(f"   Location: {job_search.get('location', 'N/A')}")
    print("\n" + "=" * 80)
    print(f"\nUsage: python run_workflow.py --config <config_name>")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI Resume Workflow Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with a specific configuration
  python run_workflow.py --config data_scientist_remote

  # List all available configurations
  python run_workflow.py --list-configs

  # Resume from a specific step
  python run_workflow.py --config ml_engineer_toronto --resume-from step3

  # Use custom config file
  python run_workflow.py --config-file my_config.yaml --config data_scientist_remote
        """
    )

    parser.add_argument(
        '--config',
        type=str,
        help='Configuration name to use'
    )

    parser.add_argument(
        '--config-file',
        type=str,
        default='workflow_config.yaml',
        help='Path to configuration file (default: workflow_config.yaml)'
    )

    parser.add_argument(
        '--list-configs',
        action='store_true',
        help='List all available configurations'
    )

    parser.add_argument(
        '--resume-from',
        type=str,
        choices=['step1', 'step2', 'step3', 'step4', 'beginning'],
        help='Resume workflow from a specific step'
    )

    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from last saved state'
    )

    args = parser.parse_args()

    if args.list_configs:
        list_configs(args.config_file)
        sys.exit(0)

    if not args.config:
        parser.print_help()
        print("\n❌ Error: --config is required (or use --list-configs)")
        sys.exit(1)

    # Create and run orchestrator
    orchestrator = WorkflowOrchestrator(
        config_name=args.config,
        config_file=args.config_file
    )

    resume_from = args.resume_from if not args.resume else None
    orchestrator.run(resume_from=resume_from)


if __name__ == "__main__":
    main()