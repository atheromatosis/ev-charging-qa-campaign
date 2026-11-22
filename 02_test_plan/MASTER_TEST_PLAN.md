# Master Test Plan – EVCC/OBC Software Release v2.4.0

**Document ID:** MTP-EVCC-2026-001  
**Version:** 1.0  
**Author:** QA Test Engineer  
**Standard Alignment:** ISTQB Foundation Level / ISO/IEC/IEEE 29119-3  
**System Under Test (SUT):** Electric Vehicle Communication Controller (EVCC) & On-Board Charger (OBC) `SW v2.4.0`  

---

## 1. Introduction & Test Objectives
This Master Test Plan defines the test strategy, scope, risk analysis, environment, and exit criteria for validating the **EVCC/OBC firmware release `v2.4.0`** prior to vehicle integration testing.

### Primary Objectives
* Verify functional compliance with `EVCC_SRS_v1.2.md` across normal, boundary, and fault-injection scenarios.
* Validate safety-critical thermal derating, connector locking, and high-voltage (HV) contactor cut-off timings.
* Verify ISO 14229 (UDS) diagnostic services (`0x19`, `0x14`) and DTC logging accuracy.
* Identify critical defects early and provide an objective **Go / No-Go** release recommendation.

---

## 2. Test Scope

### In-Scope
* **Charging State Machine:** Transitions between `Disconnected`, `Connected`, `Locked`, `Charging`, `Paused`, and `Error` (IEC 61851-1 Control Pilot states A, B, C, E/F).
* **PWM Current Negotiation:** Duty cycle calculation ($10\%–85\%$) and invalid PWM fault handling ($<8\%$, $>96\%$).
* **Thermal Management:** Current derating at $75^\circ\text{C}$ and emergency shutdown above $85^\circ\text{C}$.
* **Communication & Diagnostics:** CAN message timeout monitoring (`BMS_Status` `0x185`) and UDS DTC read/clear operations.

### Out-of-Scope
* Physical hardware stress testing (vibration, EMC, IP67 ingress protection).
* DC Fast Charging high-level communication (ISO 15118-2 / V2G PLC modem stack).
* Manufacturing End-of-Line (EOL) flashing procedures.

---

## 3. Product Risk Analysis (Risk-Based Testing)
In accordance with **ISTQB FL Chapter 5**, test effort and prioritization are driven by product risk assessment (Likelihood $\times$ Impact):

| Risk ID | Risk Description | Likelihood (1–5) | Impact (1–5) | Risk Level | Mitigation & Test Strategy |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **RSK-01** | **Arcing / Electric Shock:** Connector unlocks while HV contactors are still closed or current $> 1\text{ A}$. | 3 | 5 | **CRITICAL (15)** | Exhaustive state-transition & fault-injection tests; strict timing measurements on CAN/oscilloscope. |
| **RSK-02** | **Thermal Runaway / Fire Hazard:** OBC fails to derate at $75^\circ\text{C}$ or fails to shut down above $85^\circ\text{C}$. | 3 | 5 | **CRITICAL (15)** | Boundary Value Analysis (BVA) around $74^\circ\text{C}–86^\circ\text{C}$ with simulated NTC sensor values. |
| **RSK-03** | **Overcurrent Damage to Battery:** EVCC draws more current than BMS or cable rating allows. | 2 | 5 | **HIGH (10)** | Decision Table testing covering combinations of EVSE PWM, PP resistor, and BMS current limits. |
| **RSK-04** | **Unintended Charge Abort:** False positive CAN timeout or PWM jitter interrupts valid charging session. | 4 | 3 | **HIGH (12)** | Stability testing with nominal CAN cycle times ($100\text{ ms}$) and boundary jitter ($490\text{ ms}$ vs $510\text{ ms}$). |
| **RSK-05** | **Improper DTC Clearing:** Diagnostic tool clears fault codes while vehicle is moving or charging. | 3 | 3 | **MEDIUM (9)** | Negative UDS testing (`0x14` service) in active states verifying NRC `0x22` response. |

---

## 4. Test Approach & Design Techniques
* **Test Levels:** System Testing (black-box on HIL bench) & System Integration Testing (EVCC + simulated BMS & EVSE).
* **Test Types:** Functional, Boundary/Negative, Diagnostic (UDS), Confirmation Testing (Retesting), and Regression Testing.
* **Black-Box Techniques Applied:**
  * **Equivalence Partitioning (EP):** Valid/invalid PWM duty cycles, diagnostic session IDs.
  * **Boundary Value Analysis (BVA):** CP voltage thresholds, temperature thresholds ($74.9^\circ\text{C} / 75.0^\circ\text{C}$, $84.9^\circ\text{C} / 85.0^\circ\text{C}$), CAN timeout ($499\text{ ms} / 501\text{ ms}$).
  * **Decision Tables:** Multi-factor current arbitration (`EVSE_Limit` vs `Cable_Limit` vs `BMS_Limit`).
  * **State Transition Testing:** Full coverage of valid transitions and invalid state triggers (0-switch and 1-switch coverage).

---

## 5. Test Environment & Tools
* **Test Bench:** Closed-loop HIL Simulator simulating EVSE Control Pilot (CP), Proximity Pilot (PP), and Inlet NTC temperature sensors.
* **Bus Communication:** Vector CANoe / Python-CAN interface (`EVCC_Network_v2.dbc`, `500 kbps`).
* **Diagnostics:** UDS Diagnostic Tester (`Req ID: 0x7E2`, `Resp ID: 0x7EA`).
* **Defect & Test Management:** GitHub Issues & Markdown/CSV Test Suite artifacts.

---

## 6. Entry and Exit Criteria

### Entry Criteria (Start of Test Execution)
* `EVCC_SRS_v1.2.md` static review completed and critical ambiguities resolved (`REV-001` to `REV-004`).
* Firmware `v2.4.0` successfully flashed onto target ECU and smoke test (CAN heartbeat + UDS TesterPresent `0x3E`) passed.
* HIL test bench calibrated and `.dbc` communication matrix verified.

### Exit Criteria (Release Sign-Off)
* **100%** of planned test cases executed.
* **100%** pass rate on all **Critical** and **High** risk test cases (`RSK-01` to `RSK-04`).
* **0** open defects with Severity `Blocker` or `Critical`.
* **0** open `Major` defects without an approved workaround or mitigation plan.
* Final Test Summary Report reviewed and signed off by QA Lead and System Architect.

---

## 7. Deliverables
1. **Requirements Traceability Matrix (`RTM.md`)** – mapping all 18 requirements to test cases.
2. **Test Case Specifications (`test_cases.csv` & `state_transition_tests.md`)** – 32 executable test cases.
3. **Defect Reports (`04_defect_reports/`)** – detailed bug reports with CAN/UDS logs.
4. **Test Progress & Summary Reports (`05_test_reports/`)** – weekly status and final release decision.
