# Static Review Report – EVCC SRS v1.2
**Review Type:** Walkthrough / Technical Review (ISTQB FL Chapter 3)  
**Reviewer:** QA Test Engineer  
**Reviewed Document:** `EVCC_SRS_v1.2.md`  
**Status:** Completed – 4 Defects Logged Against Requirements  

---

## Review Summary
A static analysis of `EVCC_SRS_v1.2.md` was conducted prior to test case design to identify ambiguities, missing boundary definitions, and untestable statements.

## Identified Requirement Defects

| Review ID | Requirement ID | Defect Category | Description & Impact | Proposed Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **REV-001** | `REQ-EVCC-005` & `REQ-EVCC-006` | **Completeness / Gap** | `REQ-EVCC-005` defines behavior for $10\% \le D \le 85\%$, and `REQ-EVCC-006` defines faults for $D < 8\%$ or $D > 96\%$. Behavior for duty cycles in ranges **`8%–9.9%`** and **`85.1%–96%`** (e.g., digital communication mode 5% or high-current >63A formula) is undefined. | Clarify behavior for `8% <= D < 10%` (e.g., 6A minimum) and `85% < D <= 96%` per IEC 61851-1. |
| **REV-002** | `REQ-EVCC-010` | **Ambiguity** | The phrase *"drops to a safe level"* is subjective and cannot be objectively verified during testing. | Replace with a measurable threshold: *"until $T_{inlet} \le 60^\circ\text{C}$ with a $5^\circ\text{C}$ hysteresis."* |
| **REV-003** | `REQ-EVCC-014` | **Safety / Completeness** | Unlocking the connector while HV contactors are opening without specifying a current drop threshold (e.g., $I < 1\text{ A}$) risks electrical arcing on the DC/AC pins. | Add condition: *"Unlock actuator shall only be energized once charging current drops below `1.0 A` and HV contactors report `Open`."* |
| **REV-004** | `REQ-EVCC-008` | **Boundary Ambiguity** | Does not specify whether the `50%` current derating applies to the *maximum hardware rating* or the *currently negotiated EVSE/BMS limit*. | Specify: *"50% of the currently active negotiated current limit ($I_{max}$)."* |
