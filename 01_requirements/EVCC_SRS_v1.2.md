```markdown
# System Requirements Specification (SRS) – EVCC/OBC Module
**Document ID:** SRS-EVCC-2026-012  
**Version:** 1.2  
**Target SW Release:** v2.4.0  

---

## 1. Charging State Machine & Control Pilot (CP)
* **REQ-EVCC-001:** When the charging cable is plugged in and Control Pilot (CP) voltage transitions from `12V` (State A) to `9V` (State B), the EVCC shall transition from `Disconnected` to `Connected` within `200 ms`.
* **REQ-EVCC-002:** Upon entering the `Connected` state, the EVCC shall engage the electromechanical connector lock actuator before requesting energy transfer.
* **REQ-EVCC-003:** If the connector lock feedback signal (`Lock_Status`) does not confirm a locked state within `1500 ms`, the EVCC shall abort initialization, transition to `Error`, and log DTC `0x910412` (Connector Lock Failure).
* **REQ-EVCC-004:** When CP duty cycle is between `10%` and `85%` and CP voltage drops to `6V` (State C), the EVCC shall transition to `Charging` and close the HV DC contactors.

## 2. Current Limit Negotiation & Boundary Conditions
* **REQ-EVCC-005:** The EVCC shall calculate the maximum allowable charging current ($I_{max}$) based on the CP PWM duty cycle ($D$) using the formula: $I_{max} = D \times 0.6\text{ A}$ for $10\% \le D \le 85\%$.
* **REQ-EVCC-006:** If the CP PWM duty cycle is below `8%` or above `96%`, the EVCC shall treat the signal as invalid, open the HV contactors within `100 ms`, and enter the `Error` state.
* **REQ-EVCC-007:** The charging current drawn by the OBC shall never exceed the lowest value among: EVSE PWM limit, cable proximity pilot (PP) resistor rating, and BMS requested current limit.

## 3. Thermal Protection & Derating
* **REQ-EVCC-008:** When the charging inlet temperature ($T_{inlet}$) reaches `75°C`, the OBC shall derate the charging current by `50%`.
* **REQ-EVCC-009:** If $T_{inlet}$ exceeds `85°C`, the EVCC shall immediately terminate charging, open HV contactors, and set DTC `0x910855` (Inlet Over-Temperature).
* **REQ-EVCC-010:** After an over-temperature shutdown, the connector shall remain locked until $T_{inlet}$ drops to a safe level. *(Note: Intentional ambiguity for static review)*

## 4. Fault Handling & UDS Diagnostics (ISO 14229)
* **REQ-EVCC-011:** Loss of CAN communication with the BMS (`BMS_Status` frame, ID `0x185`) for more than `500 ms` during `Charging` shall trigger an emergency shutdown and log DTC `0xC10087` (Lost Communication with BMS).
* **REQ-EVCC-012:** The EVCC shall support UDS service `0x19` (ReadDTCInformation) and `0x14` (ClearDiagnosticInformation) in both Default Session (`0x01`) and Extended Diagnostic Session (`0x03`).
* **REQ-EVCC-013:** Service `0x14` (ClearDiagnosticInformation) shall be rejected with Negative Response Code `0x22` (ConditionsNotCorrect) if the vehicle speed is greater than `0 km/h` or if the system is currently in the `Charging` state.
* **REQ-EVCC-014:** When the user triggers the unlock button on the key fob while in `Charging` state, the EVCC shall pause charging, open HV contactors, and unlock the connector. *(Note: Intentional missing timing/current threshold for static review)*
