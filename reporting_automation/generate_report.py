import argparse
import csv
import os
import smtplib
from collections import defaultdict
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


def parse_test_results(csv_path: Path) -> list[dict]:
    """Read test cases and execution statuses from CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Test results file not found: {csv_path}")

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def calculate_metrics(test_cases: list[dict]) -> dict:
    """Compute overall and per-suite QA execution metrics."""
    total = len(test_cases)
    passed = sum(1 for tc in test_cases if tc["Status"].strip().lower() == "pass")
    failed = sum(1 for tc in test_cases if tc["Status"].strip().lower() == "fail")
    blocked = sum(1 for tc in test_cases if tc["Status"].strip().lower() == "blocked")

    pass_rate = (passed / total * 100.0) if total > 0 else 0.0

    suite_stats = defaultdict(lambda: {"total": 0, "pass": 0, "fail": 0, "blocked": 0})
    failed_cases = []

    for tc in test_cases:
        suite = tc["Test_Suite"].strip()
        status = tc["Status"].strip().lower()
        suite_stats[suite]["total"] += 1
        if status in suite_stats[suite]:
            suite_stats[suite][status] += 1
        if status == "fail":
            failed_cases.append(tc)

    # Evaluate Release Gate (Exit Criteria: 0 Failed tests & >= 95% Pass Rate)
    release_decision = "GO" if (failed == 0 and blocked == 0 and pass_rate >= 95.0) else "NO-GO"

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "blocked": blocked,
        "pass_rate": round(pass_rate, 2),
        "suite_stats": dict(suite_stats),
        "failed_cases": failed_cases,
        "release_decision": release_decision,
    }


def render_html_report(metrics: dict, release_version: str) -> str:
    """Generate an executive-ready HTML test summary report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    decision_color = "#16a34a" if metrics["release_decision"] == "GO" else "#dc2626"

    suite_rows = ""
    for suite, stats in metrics["suite_stats"].items():
        s_rate = (stats["pass"] / stats["total"] * 100.0) if stats["total"] > 0 else 0.0
        suite_rows += f"""
        <tr>
            <td><strong>{suite}</strong></td>
            <td>{stats['total']}</td>
            <td style="color:#16a34a;">{stats['pass']}</td>
            <td style="color:#dc2626;">{stats['fail']}</td>
            <td>{stats['blocked']}</td>
            <td><strong>{s_rate:.1f}%</strong></td>
        </tr>
        """

    failed_rows = ""
    for tc in metrics["failed_cases"]:
        bug_id = tc.get("Linked_Bug", "N/A") or "N/A"
        failed_rows += f"""
        <tr>
            <td><strong>{tc['Test_ID']}</strong></td>
            <td>{tc['Requirement_ID']}</td>
            <td>{tc['Title']}</td>
            <td><span class="badge-fail">{tc['Priority']}</span></td>
            <td><strong>{bug_id}</strong></td>
            <td>{tc['Actual_Result']}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QA Test Execution Report - {release_version}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; color: #1f2937; background-color: #f9fafb; }}
        .container {{ max-width: 960px; margin: auto; background: #ffffff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }}
        h1 {{ border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; color: #111827; }}
        h2 {{ margin-top: 28px; color: #374151; }}
        .summary-grid {{ display: flex; gap: 15px; margin: 20px 0; }}
        .card {{ flex: 1; padding: 15px; border-radius: 6px; background: #f3f4f6; text-align: center; }}
        .card h3 {{ margin: 0; font-size: 13px; text-transform: uppercase; color: #6b7280; }}
        .card p {{ margin: 8px 0 0; font-size: 24px; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; }}
        th, td {{ border: 1px solid #e5e7eb; padding: 10px; text-align: left; }}
        th {{ background-color: #f3f4f6; }}
        .badge-fail {{ background: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }}
        .footer {{ margin-top: 30px; font-size: 12px; color: #6b7280; text-align: right; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>EVCC/OBC QA Test Execution Report ({release_version})</h1>
        <p><strong>Generated:</strong> {timestamp} | <strong>Standard:</strong> ISTQB FL / ISO 29119</p>

        <div class="summary-grid">
            <div class="card"><h3>Total Executed</h3><p>{metrics['total']}</p></div>
            <div class="card"><h3>Passed</h3><p style="color:#16a34a;">{metrics['passed']}</p></div>
            <div class="card"><h3>Failed</h3><p style="color:#dc2626;">{metrics['failed']}</p></div>
            <div class="card"><h3>Pass Rate</h3><p>{metrics['pass_rate']}%</p></div>
            <div class="card"><h3>Release Gate</h3><p style="color:{decision_color};">{metrics['release_decision']}</p></div>
        </div>

        <h2>1. Breakdown by Test Suite</h2>
        <table>
            <thead>
                <tr>
                    <th>Test Suite</th>
                    <th>Total</th>
                    <th>Passed</th>
                    <th>Failed</th>
                    <th>Blocked</th>
                    <th>Pass Rate</th>
                </tr>
            </thead>
            <tbody>{suite_rows}</tbody>
        </table>

        <h2>2. Failed Test Cases & Linked Defects</h2>
        <table>
            <thead>
                <tr>
                    <th>Test ID</th>
                    <th>Req ID</th>
                    <th>Test Case Title</th>
                    <th>Priority</th>
                    <th>Defect ID</th>
                    <th>Observed Failure</th>
                </tr>
            </thead>
            <tbody>{failed_rows}</tbody>
        </table>

        <div class="footer">Automated QA Reporting Pipeline &bull; EVCC/OBC Validation Team</div>
    </div>
</body>
</html>
"""
    return html_content


def send_email_report(
    html_body: str,
    recipient: str,
    release_version: str,
    decision: str,
    dry_run: bool = True,
) -> None:
    """Dispatch HTML test summary report via SMTP (supports dry-run mode)."""
    subject = f"[QA Report] EVCC/OBC {release_version} - Release Gate: {decision}"

    if dry_run:
        print(f"[DRY-RUN] Email prepared for: {recipient}")
        print(f"[DRY-RUN] Subject: {subject}")
        print("[DRY-RUN] SMTP transmission skipped. Use --send-email with SMTP env vars to dispatch.")
        return

    smtp_host = os.getenv("SMTP_HOST", "smtp.example.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        if smtp_user and smtp_pass:
            server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [recipient], msg.as_string())
    print(f"[SUCCESS] Report dispatched to {recipient}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and send QA HTML test execution report.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "03_test_cases" / "test_cases.csv",
        help="Path to test_cases.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "sample_report.html",
        help="Output HTML file path",
    )
    parser.add_argument("--release", type=str, default="v2.4.0", help="Software release version")
    parser.add_argument("--recipient", type=str, default="release-board@automotive-oem.example", help="Recipient email")
    parser.add_argument("--send-email", action="store_true", help="Actually send email via SMTP (default is dry-run)")

    args = parser.parse_args()

    test_cases = parse_test_results(args.csv)
    metrics = calculate_metrics(test_cases)
    html_report = render_html_report(metrics, args.release)

    args.output.write_text(html_report, encoding="utf-8")
    print(f"[INFO] HTML report generated: {args.output}")
    print(f"[INFO] Summary: {metrics['passed']}/{metrics['total']} Passed ({metrics['pass_rate']}%) | Gate: {metrics['release_decision']}")

    send_email_report(
        html_body=html_report,
        recipient=args.recipient,
        release_version=args.release,
        decision=metrics["release_decision"],
        dry_run=not args.send_email,
    )


if __name__ == "__main__":
    main()
