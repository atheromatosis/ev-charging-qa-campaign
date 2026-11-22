# Black-Box Test Design Artifacts (ISTQB FL Chapter 4)

This document details the structured test design techniques applied to derive test cases in `test_cases.csv`.

---

## 1. Decision Table – Current Limit Arbitration (`REQ-EVCC-007`)

The EVCC must select the minimum allowed current from three independent sources: EVSE PWM duty cycle, Proximity Pilot (PP) cable coding resistor, and BMS requested limit.

| Conditions / Rules | Rule 1 (EVSE Limiting) | Rule 2 (Cable PP Limiting) | Rule 3 (BMS Limiting) | Rule 4 (Invalid PP Open) |
| :--- | :---: | :---: | :---: | :---: |
| **C1: EVSE PWM Limit** | `16 A` | `32 A` | `32 A` | `32 A` |
| **C2: Cable PP Resistor Limit** | `32 A` | `13 A` ($1500\,\Omega$) | `32 A` | `Open / Fault` |
| **C3: BMS Requested Limit** | `32 A` | `32 A` | `16 A` | `32 A` |
| **Action: Target OBC Current** | **`16 A`** | **`13 A`** | **`16 A`** | **`0 A` (Abort)** |
| **Mapped Test Case** | `TC-001 / Nominal` | **`TC-010` (FAILED)** | **`TC-009` (PASSED)** | `TC-003` |

---

## 2. State Transition Table – EVCC Charging Controller (`REQ-EVCC-001` to `004`, `014`)

0-Switch coverage ensuring every valid state transition and critical invalid trigger is tested.

| Current State | Event / Trigger | Guard Condition | Next State | Output / Action | Test Case ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Disconnected` | `CP_Voltage = 9V` (State B) | No active DTCs | `Connected` | Transition $\le 200\text{ ms}$ | `TC-001` |
| `Connected` | `Entry Action` | Cable detected | `Locked` | Engage lock actuator $\le 1500\text{ ms}$ | `TC-002` |
| `Connected` | `Lock_Timeout` ($>1500\text{ ms}$) | `Lock_Status != Locked` | `Error` | Log DTC `0x910412` | `TC-003` |
| `Locked` | `CP_Voltage = 6V` (State C) | `10% <= PWM <= 85%` | `Charging` | Close HV contactors | `TC-004` |
| `Charging` | `PWM < 8%` or `PWM > 96%` | Active energy transfer | `Error` | Open HV contactors $\le 100\text{ ms}$ | `TC-007`, `TC-008` |
| `Charging` | `T_inlet > 85°C` | NTC sensor valid | `Error` | Open HV contactors; log `0x910855` | `TC-013` |
| `Charging` | `KeyFob_Unlock` | User request | `Disconnected` | Stop current ($<1\text{ A}$), open HV, unlock | `TC-020` |
| `Error` | `T_inlet <= 60°C` & `Unplug` | Fault cleared | `Disconnected` | Release connector lock | `TC-014` |
