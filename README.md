# 🇵🇭 Philippine Payroll & Tax Computation System

A dual-language implementation of a Philippine employee payroll and income-tax computation system, built for an **MCO 1 (Ventures)** programming exercise.

---

## Project Structure

```
MCO 1 (Ventures)/
├── payroll_python/
│   └── payroll_system.py       ← Python (Procedural, CLI)
└── payroll_javascript/
    └── payroll_system.html     ← JavaScript + HTML (GUI, browser-based)
```

---

## What It Computes

| Deduction | Applies To | Rate / Basis |
|---|---|---|
| **SSS** | Private employees | 4.5% of MSC (2024 Table) |
| **GSIS** | Government employees | 9% of basic salary |
| **PhilHealth** | All employees | 2.5% employee share (5% total, min ₱500 / max ₱5,000) |
| **Pag-IBIG (HDMF)** | All employees | 1–2%, capped at ₱100/month |
| **BIR Withholding Tax** | All employees | TRAIN Law 2023+ progressive brackets |

### BIR TRAIN Law Tax Brackets

| Annual Taxable Income | Tax Due |
|---|---|
| Up to ₱250,000 | **0%** (exempt) |
| ₱250,001 – ₱400,000 | 15% of excess over ₱250,000 |
| ₱400,001 – ₱800,000 | ₱22,500 + 20% of excess over ₱400,000 |
| ₱800,001 – ₱2,000,000 | ₱102,500 + 25% of excess over ₱800,000 |
| ₱2,000,001 – ₱8,000,000 | ₱402,500 + 30% of excess over ₱2,000,000 |
| Over ₱8,000,000 | ₱2,202,500 + 35% of excess over ₱8,000,000 |

---

## Inputs (Same for Both Implementations)

| Field | Description |
|---|---|
| Employee Name | Full name of the employee |
| Employee Type | `private` (SSS) or `government` (GSIS) |
| Basic Monthly Salary | Gross basic pay (PHP) |
| Non-Taxable Allowances | De minimis/other exempt allowances (PHP) |

## Outputs (Same for Both Implementations)

- SSS **or** GSIS contribution
- PhilHealth contribution
- Pag-IBIG contribution
- Taxable monthly income
- BIR withholding tax (monthly & annual)
- Total deductions
- **Net Pay (Take-Home Pay)**
- Annualized summary table

---

## How to Run

### Python (Procedural — CLI)

> Requires Python 3.7+

```bash
python payroll_python/payroll_system.py
```

Follow the on-screen prompts to enter employee data. The payslip is printed to the terminal.

### JavaScript (GUI — Browser)

No installation required. Simply open the HTML file in any modern browser:

```
payroll_javascript/payroll_system.html
```

Fill in the form, click **⚡ Compute Payroll**, and view the interactive pay slip and annualized summary.

---

## Design Notes

| Aspect | Python | JavaScript |
|---|---|---|
| **Paradigm** | Procedural (functions only, no OOP) | Procedural (same logic structure) |
| **Interface** | CLI / Terminal | HTML + CSS GUI |
| **Same Inputs?** | ✅ Yes | ✅ Yes |
| **Same Outputs?** | ✅ Yes | ✅ Yes |
| **BIR Computation** | Annualize → compute → de-annualize | Same algorithm |
| **SSS Lookup** | Linear scan of MSC table | Same table, same scan |

---

## Disclaimer

> This system is for **educational and reference purposes only**.  
> Always consult a licensed accountant or the BIR, SSS, PhilHealth, and Pag-IBIG official portals for official computations and current rates.
