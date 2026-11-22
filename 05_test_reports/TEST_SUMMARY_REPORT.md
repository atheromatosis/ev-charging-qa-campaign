# Test Summary Report – EVCC/OBC Release v2.4.0

**Document ID:** TSR-EVCC-2026-001  
**Target Release:** `SW v2.4.0` (with Hotfix Verification on `v2.4.1-rc1`)  
**Standard Alignment:** ISTQB Foundation Level / ISO/IEC/IEEE 29119-3  
**Final Release Recommendation:** **NO-GO (REJECTED FOR VEHICLE INTEGRATION)**  

---

## 1. Executive Summary
System and integration testing for the **EVCC/OBC firmware (`v2.4.0`)** has been completed against `EVCC_SRS_v1.2.md` and `MASTER_TEST_PLAN.md`. 

Out of **20 planned test cases**, **16 Passed (`80.0%`)** and **4 Failed (`20.0%`)**, uncovering **4 defects** (`1 Critical`, `3 Major`). While `BUG-004` was resolved and verified in hotfix candidate `v2.4.1-rc1`, **three open defects remain**, including a **Critical release blocker (`BUG-003`)** affecting connector unlocking after thermal shutdown.

Consequently, **Release `v2.4.0` does NOT meet the defined Exit Criteria** and is recommended as **NO-GO**.

---

## 2. Test Execution Summary & Metrics

| Metric | Target | Actual | Status |
| :--- | :---: | :---: | :---: |
| **Requirements Coverage** | 100% (`14 / 14`) | 100% (`14 / 14`) | **MET** |
| **Test Case Execution Rate** | 100% (`20 / 20`) | 100% (`20 / 20`) | **MET** |
| **Overall Pass Rate** | $\ge 95.0\%$ | `80.0%` (`16 / 20`) | **NOT MET** |
| **Critical / High Risk Pass Rate** | `100%` | `76.5%` (`13 / 17`) | **NOT MET** |
| **Open Blocker / Critical Defects** | `0` | `1` (`BUG-003`) | **NOT MET** |
| **Open Major Defects (Unmitigated)** | `0` | `2` (`BUG-001`, `BUG-002`) | **NOT MET** |

### Results by Test Suite

| Test Suite | Total | Passed | Failed | Pass Rate | Associated Open Defects |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `TS01_StateMachine` | 5 | 5 | 0 | **100.0%** | None |
| `TS02_CurrentNegotiation` | 6 | 4 | 2 | **66.7%** | `BUG-001`, `BUG-002` |
| `TS03_ThermalProtection` | 4 | 3 | 1 | **75.0%** | `BUG-003` |
| `TS04_CAN_Diagnostics` | 5 | 4 | 1 | **80.0%** | None (`BUG-004` Closed) |
| **TOTAL** | **20** | **16** | **4** | **80.0%** | **3 Open Defects** |

---

## 3. Residual Product Risk Assessment
Deploying `SW v2.4.0` to prototype vehicles introduces unacceptable safety and usability risks:
1. **Vehicle Immobilization (`RSK-01` / `BUG-003` – CRITICAL):** Following an over-temperature event ($>85^\circ\text{C}$), the charging plug remains permanently locked even after cooling to ambient temperature, stranding the vehicle at the EVSE.
2. **Cable Thermal Overload (`RSK-03` / `BUG-002` – MAJOR):** Ignoring the Proximity Pilot (`PP`) resistor allows the OBC to draw `32 A` through a `13 A` rated cable, creating a fire hazard.
3. **HV Cut-Off Timing Violation (`RSK-01` / `BUG-001` – MAJOR):** Delayed contactor opening (`142 ms` vs `100 ms` limit) on invalid high PWM signals violates IEC 61851-1 safety timing margins.

---

## 4. Exit Criteria Evaluation & Sign-Off Decision

| Exit Criterion (from `MASTER_TEST_PLAN.md`) | Evaluation |
| :--- | :---: |
| 100% of planned test cases executed | **PASS** |
| 100% pass rate on Critical and High risk test cases | **FAIL** |
| 0 open defects with Severity `Blocker` or `Critical` | **FAIL** |
| 0 open `Major` defects without an approved workaround | **FAIL** |

### Required Actions Before Next Release Gate (`v2.4.2`)
1. Embedded SW team to resolve `BUG-003` (reset `Thermal_Lock_Latch` at $T_{inlet} \le 60^\circ\text{C}$), `BUG-002` (include `PP_CableLimit` in `min()` current arbitration), and `BUG-001` (optimize PWM fault ISR latency).
2. QA team to execute full confirmation testing (`TC-008`, `TC-010`, `TC-014`) and a regression test pass across `TS01–TS04`.
