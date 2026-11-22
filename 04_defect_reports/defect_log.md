```
# Defect Log – EVCC/OBC Release v2.4.0

**Total Defects Logged:** 4 (`1 Critical`, `3 Major`)  
**Open Defects:** 3 (`BUG-001`, `BUG-002`, `BUG-003`)  
**Closed Defects:** 1 (`BUG-004` – verified in hotfix branch `v2.4.1-rc1`)  

---

## BUG-001: HV Contactors Opening Time Exceeds 100 ms Limit on High PWM Fault (>96%)

* **Status:** `Open` (Assigned to Embedded SW Team)
* **Severity:** `Major` (Timing violation of safety requirement `REQ-EVCC-006`)
* **Priority:** `P2 - High`
* **Linked Requirement:** `REQ-EVCC-006` | **Linked Test Case:** `TC-008`
* **Environment:** `EVCC SW v2.4.0` | `HIL Bench #2` | `EVCC_Network_v2.dbc`

### Description
When the EVSE Control Pilot (CP) PWM duty cycle transitions from a valid charging state (`53.3%`) to an out-of-range high value (`96.1%`), the EVCC correctly detects the fault and opens the HV contactors, but the cut-off time is **`142 ms`**, violating the maximum allowed **`100 ms`** threshold.

### Steps to Reproduce
1. Establish an active `Charging` session (`CP = 6V`, `PWM = 53.3%`, `32A`).
2. Inject PWM duty cycle step change to `96.1%` via HIL signal generator.
3. Measure delta time ($\Delta t$) between PWM fault injection and `HV_Contactor_Status == Open` on CAN.

### Expected Result
HV contactors open within $\le 100\text{ ms}$ and `EVCC_State` transitions to `Error`.

### Actual Result
HV contactors opened after `142 ms` (`+42 ms` over specification limit).

### Diagnostic Evidence (CAN Trace)
```text
[12.400.000] CAN1  0x210  8  06 53 01 00 00 00 00 00  # CP_Volt=6V, PWM=53.3%, HV_Contactor=Closed
[12.410.000] HIL   ---    -  -- -- -- -- -- -- -- --  # INJECT: CP_PWM = 96.1%
[12.552.000] CAN1  0x210  8  06 96 00 04 00 00 00 00  # HV_Contactor=Open, EVCC_State=Error (Delta = 142 ms)

---

## BUG-002: OBC Ignores Proximity Pilot (PP) Cable Current Limit During Arbitration

* **Status:** `Open`
* **Severity:** `Major` (Risk of cable overheating on 13A/20A rated Type 2 cables)
* **Priority:** `P2 - High`
* **Linked Requirement:** `REQ-EVCC-007` | **Linked Test Case:** `TC-010`
* **Environment:** `EVCC SW v2.4.0` | `HIL Bench #2` | `EVCC_Network_v2.dbc`

### Description
During current arbitration, the EVCC evaluates `EVSE_PWM_Limit` and `BMS_MaxCurrent`, but ignores the Proximity Pilot (`PP`) resistor rating (`1500 Ohm` = `13 A` cable limit), allowing the OBC to draw `32 A`.

### Steps to Reproduce
1. Configure HIL PP resistor simulation to `1500 Ohm` (`13 A` max cable capacity).
2. Set EVSE PWM limit to `32 A` (`53.3%`) and BMS requested limit to `32 A`.
3. Transition to `Charging` state and read `EVCC_MaxCurrent` on CAN ID `0x212`.

### Expected Result
`EVCC_MaxCurrent` is arbitrated to `13.0 A` ($\min(32\text{ A}, 13\text{ A}, 32\text{ A})$).

### Actual Result
`EVCC_MaxCurrent` is broadcast as `32.0 A`, overloading the simulated `13 A` cable.

### Diagnostic Evidence (CAN Trace)
```text
[45.100.000] CAN1  0x185  8  40 01 00 00 00 00 00 00  # BMS_MaxCurrent = 32.0 A
[45.110.000] CAN1  0x211  8  0D 20 00 00 00 00 00 00  # PP_CableLimit = 13.0 A (0x0D), EVSE_Limit = 32.0 A (0x20)
[45.120.000] CAN1  0x212  8  20 00 00 00 00 00 00 00  # EVCC_MaxCurrent = 32.0 A (0x20) -> EXPECTED 0x0D!

---

## BUG-003: Connector Remains Permanently Locked After Over-Temperature Shutdown Cool-Down

* **Status:** `Open` (**RELEASE BLOCKER**)
* **Severity:** `Critical` (Vehicle stranded at charging station; cable cannot be removed without manual emergency release)
* **Priority:** `P1 - Urgent`
* **Linked Requirement:** `REQ-EVCC-010` | **Linked Test Case:** `TC-014`
* **Environment:** `EVCC SW v2.4.0` | `HIL Bench #2` | `EVCC_Network_v2.dbc`

### Description
After an inlet over-temperature emergency shutdown ($T_{inlet} > 85^\circ\text{C}$, DTC `0x910855`), the connector lock actuator fails to release even after the inlet temperature cools down below `60°C` (tested down to `25°C`) and a key fob unlock command is issued. Only a hard KL30 battery reset clears the lock state.

### Steps to Reproduce
1. Trigger over-temperature shutdown by setting simulated `T_inlet = 85.1°C` during charging (`TC-013`).
2. Verify `EVCC_State == Error` and `Lock_Status == Locked`.
3. Reduce simulated `T_inlet` to `58.0°C` (and further to `25.0°C`).
4. Trigger `KeyFob_Unlock` signal on CAN.

### Expected Result
Once $T_{inlet} \le 60^\circ\text{C}$, `KeyFob_Unlock` disengages the connector lock (`Lock_Status == Unlocked`).

### Actual Result
`Lock_Status` remains `Locked` indefinitely; `Lock_Actuator_Cmd` is never triggered.

### Root Cause Note (Developer Feedback)
The `Thermal_Lock_Latch` boolean flag is set in the `Error` state entry handler, but the reset condition in the cyclic `10 ms` task checks `EVCC_State == Disconnected` instead of `T_inlet <= 60.0°C`, creating a deadlock.

---

## BUG-004: UDS ClearDiagnosticInformation (0x14) Accepted While Vehicle Speed > 0 km/h

* **Status:** `Closed` (Verified Fixed in `v2.4.1-rc1`)
* **Severity:** `Major` (Regulatory / Diagnostic safety compliance failure)
* **Priority:** `P2 - High`
* **Linked Requirement:** `REQ-EVCC-013` | **Linked Test Case:** `TC-019`
* **Environment:** `EVCC SW v2.4.0` $\rightarrow$ Retested on `v2.4.1-rc1`

### Description
Sending UDS service `0x14 0xFF 0xFF 0xFF` while the vehicle is in motion (`Vehicle_Speed = 15 km/h`) clears stored DTCs instead of rejecting the request with Negative Response Code `0x22` (`ConditionsNotCorrect`).

### Steps to Reproduce
1. Ensure at least one historical DTC (`0x910412`) is stored in ECU memory.
2. Set `Vehicle_Speed = 15 km/h` on CAN frame `0x100`.
3. Send physical UDS request `0x14 0xFF 0xFF 0xFF` on CAN ID `0x7E2`.

### Expected Result
ECU responds on `0x7EA` with Negative Response `0x7F 0x14 0x22` (`ConditionsNotCorrect`).

### Actual Result (v2.4.0)
ECU responded with Positive Response `0x54` and erased all DTCs while vehicle was moving.

### Diagnostic Evidence (UDS Trace – v2.4.0)
```text
[88.200.000] CAN1  0x100  8  00 96 00 00 00 00 00 00  # Vehicle_Speed = 15.0 km/h (0x0096 * 0.1)
[88.210.000] CAN1  0x7E2  8  04 14 FF FF FF 00 00 00  # UDS Req: ClearDiagnosticInformation
[88.215.000] CAN1  0x7EA  8  01 54 00 00 00 00 00 00  # UDS Resp: Positive Response (FAIL!)
```

### Confirmation & Regression Testing Notes (v2.4.1-rc1)
* **Retest Result (`TC-019`):** Flashed `v2.4.1-rc1` on HIL Bench #2. Sent `0x14 0xFF 0xFF 0xFF` at `15 km/h` $\rightarrow$ ECU properly returned `0x7F 0x14 0x22`.
* **Regression Check (`TC-017`, `TC-018`):** Verified `0x14` still succeeds when `Vehicle_Speed == 0 km/h` and `EVCC_State == Disconnected`. Defect marked as **`Closed`**.
