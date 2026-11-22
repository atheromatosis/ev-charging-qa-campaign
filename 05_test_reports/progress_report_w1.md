# Weekly Test Progress Report – Week 1
**Project:** EVCC/OBC Firmware Validation (`Release v2.4.0`)  
**Reporting Period:** 2026-11-09 – 2026-11-13  
**Author:** QA Test Engineer  
**Distribution:** Project Manager, System Architect, Embedded SW Lead  

---

## 1. Executive Status Summary
* **Overall Test Health:** **AMBER (At Risk)**
* **Test Execution Progress:** `12 / 20` planned test cases executed (`60.0%`)
* **Key Highlight:** Core Charging State Machine (`TS01`) passed nominal transition timing checks.
* **Key Blocker / Risk:** Two `Major` defects (`BUG-001`, `BUG-002`) identified in PWM fault cut-off timing and PP cable current limit arbitration.

---

## 2. Execution Metrics Breakdown (Week 1)

| Test Suite | Planned | Executed | Passed | Failed | Blocked | Pass Rate (Executed) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `TS01_StateMachine` | 5 | 5 | 5 | 0 | 0 | **100.0%** |
| `TS02_CurrentNegotiation` | 6 | 6 | 4 | 2 | 0 | **66.7%** |
| `TS03_ThermalProtection` | 4 | 1 | 1 | 0 | 0 | **100.0%** |
| `TS04_CAN_Diagnostics` | 5 | 0 | 0 | 0 | 0 | **N/A** |
| **TOTAL** | **20** | **12** | **10** | **2** | **0** | **83.3%** |

---

## 3. Defects Logged This Week
* **`BUG-001` (Major / P2):** HV contactors opening time measured at `142 ms` on high PWM fault (`96.1%`), exceeding the `100 ms` safety limit (`REQ-EVCC-006`).
* **`BUG-002` (Major / P2):** OBC ignores Proximity Pilot (`PP`) `1500 Ohm` (`13 A`) cable rating and draws `32 A` (`REQ-EVCC-007`).

---

## 4. Plan for Next Week (Week 2)
1. Complete execution of `TS03_ThermalProtection` (`TC-012` to `TC-014`) on HIL Bench #2.
2. Execute `TS04_CAN_Diagnostics` (`TC-015` to `TC-019`) verifying BMS CAN timeout and UDS services `0x19` / `0x14`.
3. Perform confirmation testing (retests) on any hotfix builds delivered by the SW team.
