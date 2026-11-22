# EV Charging Controller (EVCC/OBC) – QA Test Campaign

![ISTQB](https://img.shields.io/badge/Standard-ISTQB%20FL%20%2F%20ISO%2029119-blue)
![Domain](https://img.shields.io/badge/Domain-Automotive%20EV%20Charging-green)
![Protocol](https://img.shields.io/badge/Diagnostics-UDS%20%2F%20CAN-orange)
![Automation](https://img.shields.io/badge/Reporting-Python%203.11-yellow)

## Project Overview

This repository demonstrates an end-to-end **Software Testing Life Cycle (STLC)** campaign for an **Electric Vehicle Communication Controller (EVCC)** and **On-Board Charger (OBC)** module (`SW Release v2.4.0`).

The project is structured according to **ISTQB Foundation Level** principles and **ISO/IEC/IEEE 29119** test documentation standards, showcasing:
* **Static Testing:** Requirements review and ambiguity detection (Shift-Left approach).
* **Risk-Based Test Planning:** Product risk analysis, entry/exit criteria, and test environment setup.
* **Black-Box Test Design:** Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Decision Tables, and State Transition Testing.
* **Defect Management:** Full bug lifecycle tracking with CAN/UDS diagnostic evidence, severity/priority triage, retesting, and regression verification.
* **Test Reporting & Automation:** Progress reports, final Go/No-Go summary report, and a Python-based automated HTML/Email reporting pipeline.

---

## System Under Test (SUT) Architecture

The EVCC/OBC module manages the AC/DC charging session between the Electric Vehicle Supply Equipment (EVSE) and the High-Voltage Battery Management System (BMS).

```mermaid
stateDiagram-v2
    [*] --> Disconnected
    Disconnected --> Connected : CP_State_B (Cable Plugged)
    Connected --> Locked : Connector_Lock_Engaged
    Locked --> Charging : CP_State_C + PWM_Valid
    Charging --> Paused : EVSE_Suspend / User_Pause
    Paused --> Charging : Resume_Command
    Charging --> Error : OverTemp / CAN_Timeout / Pilot_Fault
    Locked --> Error : Lock_Mechanism_Fault
    Error --> Disconnected : Fault_Cleared & Cable_Unplugged
    Locked --> Disconnected : Charge_Complete & Unlocked
