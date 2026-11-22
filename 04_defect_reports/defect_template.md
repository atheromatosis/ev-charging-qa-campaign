# Defect Report Template (ISTQB / ISO 29119-3 Compliant)

* **Defect ID:** `BUG-XXX`
* **Summary / Title:** `[Component] Short, concise description of the failure`
* **Status:** `New` | `Open` | `In Progress` | `Fixed` | `Retest` | `Closed` | `Deferred`
* **Severity (Technical Impact):** `Blocker` | `Critical` | `Major` | `Minor` | `Trivial`
* **Priority (Business Urgency):** `P1 - Urgent` | `P2 - High` | `P3 - Medium` | `P4 - Low`
* **Linked Requirement:** `REQ-EVCC-XXX`
* **Linked Test Case:** `TC-XXX`
* **Environment:** `SW Version` | `HW Revision` | `HIL Bench / DBC Version`

## Description
Detailed explanation of the anomaly observed during test execution.

## Preconditions
System state and configuration required before executing reproduction steps.

## Steps to Reproduce
1. Step one...
2. Step two...
3. Step three...

## Expected Result
Behavior defined in the System Requirements Specification (SRS).

## Actual Result
Observed behavior of the System Under Test (SUT).

## Diagnostic Evidence (CAN / UDS Trace)
```text
[Timestamp]  Channel  ID     DLC  Data Bytes                Decoded Signal / Meaning
