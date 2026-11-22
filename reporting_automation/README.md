# Automated QA Test Reporting Pipeline

This module automates the generation and distribution of executive QA Test Execution Reports directly from the structured test suite (`03_test_cases/test_cases.csv`).

## Features
* Parses CSV test execution results (`Pass`, `Fail`, `Blocked`) and linked defect IDs (`BUG-XXX`).
* Automatically evaluates release gate criteria (`GO` vs `NO-GO`).
* Generates a self-contained HTML dashboard (`sample_report.html`) with per-suite metrics and failure breakdown.
* Supports automated SMTP email dispatching to stakeholders (`--send-email`) with safe `--dry-run` default mode.

## Usage

Run from the repository root to generate `sample_report.html` and preview the email dispatch:

```bash
python3 reporting_automation/generate_report.py --release v2.4.0 --recipient qa-lead@example.com
```

To send the report via a real SMTP server, configure environment variables and pass `--send-email`:

```bash
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@example.com"
export SMTP_PASS="your-app-password"

python3 reporting_automation/generate_report.py --send-email --recipient manager@example.com
```
