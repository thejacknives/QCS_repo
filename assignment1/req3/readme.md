# Tyre Pressure Warning – Fault Tolerant System

This folder contains the implementation of the **FR3 - Tyre Pressure Warning** functionality, with fault tolerance mechanisms applied, as well as a setup to simulate **N-Version Programming**.

## Running the Fault-Tolerant Version Only

To run just the fault-tolerant version of the system, execute: 'req3_Fault.py'


This will run several test cases and apply all fault-tolerant mechanisms such as input validation, outlier detection, and DMR.

---

## Running N-Version Programming (NVP) Comparator

To run the N-Version Programming comparator (which runs both implementations and compares results), execute: 'nvp_runner.py'


This will:
- Run both the fault-tolerant implementation and the baseline version
- Compare the outputs
- Show warnings if there are mismatches
- Save results to `ft_output.txt` and `v2_output.txt`

---

## Ignore This File

**`Re3_tomas_tavares`**

This file contains a baseline version of the tyre pressure warning logic, written by another group. It is **used strictly for N-Version Programming simulation purposes** and should not be modified or run directly. It does **not contain any fault-tolerant logic**.

---

## Files in this folder:

| File              | Description                                                       |
|-------------------|-------------------------------------------------------------------|
| `req3_Fault.py` | Main fault-tolerant implementation                              |
| `Re3_tomas_tavares.py`             | Baseline version used for N-Version comparison (do not edit)    |
| `nvp_runner.py`     | Script that runs both versions and compares outputs             |
| `ft_output.txt`     | Output of fault-tolerant version (after `nvp_runner.py` runs)   |
| `v2_output.txt`     | Output of baseline version (after `nvp_runner.py` runs)         |
