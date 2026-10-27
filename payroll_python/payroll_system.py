"""
================================================================================
PHILIPPINE EMPLOYEE PAYROLL & TAX COMPUTATION SYSTEM
================================================================================
Programming Language : Python (Procedural)
Description          : Computes SSS, PhilHealth, Pag-IBIG, GSIS, and BIR
                       Income Tax for Philippine employees (TRAIN Law 2023+).
Rates Effective      : January 1, 2025
  - SSS  : Circular No. 2024-006 | Rate 5% | MSC ₱5,000–₱35,000
  - PhilHealth : Advisory 2025-0002 | Rate 5% | Floor ₱10k / Ceiling ₱100k
  - Pag-IBIG   : Circular No. 460 | Max ₱200/mo | MFS ₱10,000
  - GSIS : RA 8291 | Employee share 9%
  - BIR  : TRAIN Law (RA 10963) progressive brackets
Author               : MCO 1 - Ventures
Date                 : 2025
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
#  CONSTANTS & RATE TABLES
# ─────────────────────────────────────────────────────────────────────────────

# --- SSS Monthly Salary Credit (MSC) Table (2025) ---
# SSS Circular No. 2024-006 — effective January 1, 2025
# Rate: 15% total (Employee: 5%, Employer: 10%)
# Min MSC: ₱5,000 | Max MSC: ₱35,000
# Each entry: (min_salary, max_salary, msc)
SSS_table = [
    (0,      5249.99,  5000),
    (5250,   5749.99,  5500),
    (5750,   6249.99,  6000),
    (6250,   6749.99,  6500),
    (6750,   7249.99,  7000),
    (7250,   7749.99,  7500),
    (7750,   8249.99,  8000),
    (8250,   8749.99,  8500),
    (8750,   9249.99,  9000),
    (9250,   9749.99,  9500),
    (9750,  10249.99, 10000),
    (10250, 10749.99, 10500),
    (10750, 11249.99, 11000),
    (11250, 11749.99, 11500),
    (11750, 12249.99, 12000),
    (12250, 12749.99, 12500),
    (12750, 13249.99, 13000),
    (13250, 13749.99, 13500),
    (13750, 14249.99, 14000),
    (14250, 14749.99, 14500),
    (14750, 15249.99, 15000),
    (15250, 15749.99, 15500),
    (15750, 16249.99, 16000),
    (16250, 16749.99, 16500),
    (16750, 17249.99, 17000),
    (17250, 17749.99, 17500),
    (17750, 18249.99, 18000),
    (18250, 18749.99, 18500),
    (18750, 19249.99, 19000),
    (19250, 19749.99, 19500),
    (19750, 20249.99, 20000),
    (20250, 20749.99, 20500),
    (20750, 21249.99, 21000),
    (21250, 21749.99, 21500),
    (21750, 22249.99, 22000),
    (22250, 22749.99, 22500),
    (22750, 23249.99, 23000),
    (23250, 23749.99, 23500),
    (23750, 24249.99, 24000),
    (24250, 24749.99, 24500),
    (24750, 25249.99, 25000),
    (25250, 25749.99, 25500),
    (25750, 26249.99, 26000),
    (26250, 26749.99, 26500),
    (26750, 27249.99, 27000),
    (27250, 27749.99, 27500),
    (27750, 28249.99, 28000),
    (28250, 28749.99, 28500),
    (28750, 29249.99, 29000),
    (29250, 29749.99, 29500),
    (29750, 30249.99, 30000),
    (30250, 30749.99, 30500),
    (30750, 31249.99, 31000),
    (31250, 31749.99, 31500),
    (31750, 32249.99, 32000),
    (32250, 32749.99, 32500),
    (32750, 33249.99, 33000),
    (33250, 33749.99, 33500),
    (33750, 34249.99, 34000),
    (34250, 34749.99, 34500),
    (34750, float('inf'), 35000),
]
SSS_employee_rate = 0.05         # 5% employee share (2025)

# --- PhilHealth (2025) ---
Philhealth_rate           = 0.05    # 5% total premium
Philhealth_employee_share = 0.5     # Employee pays half (2.5%)
Philhealth_min_premium    = 500.00  # minimum monthly premium (salary floor 10,000)
Philhealth_max_premium    = 5000.00 # maximum monthly premium (salary ceiling 100,000)
Philhealth_floor_salary   = 10000.00
Philhealth_ceiling_salary = 100000.00

# --- Pag-IBIG (HDMF) — Pag-IBIG Circular No. 460 (2025) ---
Pagibig_rate_low  = 0.01     # 1% for salary ≤ 1,500
Pagibig_rate_high = 0.02     # 2% for salary > 1,500
Pagibig_MFS       = 10000.00 # Maximum Fund Salary (raised from ₱5,000)
Pagibig_max       = 200.00   # Max employee share: 2% × ₱10,000 = ₱200

# --- GSIS (Government employees only) ---
GSIS_employee_rate = 0.09  # 9% employee share

# --- BIR / TRAIN Law Income Tax Brackets (Annual) ---
# (excess_over, base_tax, rate_on_excess)
BIR_brackets = [
    (0,           0,          0.00),   # 0 – 250,000         : 0%
    (250000,      0,          0.15),   # 250,001 – 400,000   : 15%
    (400000,      22500,      0.20),   # 400,001 – 800,000   : 20%
    (800000,      102500,     0.25),   # 800,001 – 2,000,000 : 25%
    (2000000,     402500,     0.30),   # 2,000,001 – 8,000,000 : 30%
    (8000000,     2202500,    0.35),   # Over 8,000,000      : 35%
]
BIR_thresholds  = [0, 250000, 400000, 800000, 2000000, 8000000]


# ─────────────────────────────────────────────────────────────────────────────
#  COMPUTATION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def compute_sss(monthly_salary):
    """Compute SSS employee monthly contribution based on 2025 MSC table."""
    for (min_s, max_s, msc) in SSS_table:
        if min_s <= monthly_salary <= max_s:
            return round(msc * SSS_employee_rate, 2)
    return round(35000 * SSS_employee_rate, 2)  # fallback max


def compute_philhealth(monthly_salary):
    """Compute PhilHealth employee monthly contribution."""
    if monthly_salary <= Philhealth_floor_salary:
        premium = Philhealth_min_premium
    elif monthly_salary >= Philhealth_ceiling_salary:
        premium = Philhealth_max_premium
    else:
        premium = monthly_salary * Philhealth_rate
    return round(premium * Philhealth_employee_share, 2)


def compute_pagibig(monthly_salary):
    """Compute Pag-IBIG employee monthly contribution (2025 rates)."""
    # Contribution is based on salary up to the MFS cap of ₱10,000
    base = min(monthly_salary, Pagibig_MFS)
    if monthly_salary <= 1500:
        contribution = base * Pagibig_rate_low
    else:
        contribution = base * Pagibig_rate_high
    return round(min(contribution, Pagibig_max), 2)


def compute_gsis(monthly_salary):
    """Compute GSIS employee monthly contribution (government employees only)."""
    return round(monthly_salary * GSIS_employee_rate, 2)


def compute_bir_annual(annual_taxable_income):
    """
    Compute annual income tax using TRAIN Law brackets.
    Returns the annual income tax due.
    """
    if annual_taxable_income <= 0:
        return 0.00

    tax = 0.00
    for i in range(len(BIR_thresholds) - 1, -1, -1):  
        if annual_taxable_income > BIR_thresholds[i]:
            excess_over, base_tax, rate = BIR_brackets[i]
            tax = base_tax + (annual_taxable_income - excess_over) * rate
            break

    return round(tax, 2)


def compute_monthly_bir(monthly_taxable_income):
    """Compute monthly withholding tax (annualize → compute → de-annualize)."""
    annual = monthly_taxable_income * 12
    annual_tax = compute_bir_annual(annual)
    return round(annual_tax / 12, 2)


def compute_payroll(employee_type, monthly_salary, allowances=0):
    """
    Master payroll computation function.

    Parameters
    ----------
    employee_type  : str  – 'private' or 'government'
    monthly_salary : float – Basic monthly salary
    allowances     : float – Non-taxable allowances (default 0)

    Returns
    -------
    dict with all computed values
    """
    # ----- Mandatory Deductions -----
    sss         = compute_sss(monthly_salary)    if employee_type == 'private'    else 0.00
    gsis        = compute_gsis(monthly_salary)   if employee_type == 'government' else 0.00
    philhealth  = compute_philhealth(monthly_salary)
    pagibig     = compute_pagibig(monthly_salary)
 
    total_mandatory = round(sss + gsis + philhealth + pagibig, 2)

    # ----- Taxable Income -----
    # Taxable = Gross Pay - Mandatory Contributions - Non-taxable Allowances
    gross_pay       = monthly_salary + allowances
    taxable_income  = monthly_salary - total_mandatory
    taxable_income  = max(taxable_income, 0)

    # ----- Withholding Tax (BIR) -----
    withholding_tax = compute_monthly_bir(taxable_income)

    # ----- Net Pay -----
    total_deductions = round(total_mandatory + withholding_tax, 2)
    net_pay          = round(gross_pay - total_deductions, 2)

    return {
        "employee_type"     : employee_type.capitalize(),
        "gross_pay"         : gross_pay,
        "monthly_salary"    : monthly_salary,
        "allowances"        : allowances,
        "sss"               : sss,
        "gsis"              : gsis,
        "philhealth"        : philhealth,
        "pagibig"           : pagibig,
        "total_mandatory"   : total_mandatory,
        "taxable_income"    : taxable_income,
        "withholding_tax"   : withholding_tax,
        "total_deductions"  : total_deductions,
        "net_pay"           : net_pay,
    }


# ─────────────────────────────────────────────────────────────────────────────
#  DISPLAY / UI FUNCTIONS (Procedural CLI)
# ─────────────────────────────────────────────────────────────────────────────

def print_separator(char="─", width=60):
    print(char * width)


def print_header():
    print_separator("═")
    print("  PHILIPPINE EMPLOYEE PAYROLL & TAX COMPUTATION SYSTEM")
    print("  BIR | SSS | PhilHealth | Pag-IBIG | GSIS  (TRAIN Law)")
    print_separator("═")
    print()


def print_payslip(result, employee_name):
    """Pretty-print the computed payroll result."""
    print()
    print_separator("═")
    print("                      PAY SLIP")
    print_separator("═")
    print(f"  Employee Name   : {employee_name}")
    print(f"  Employee Type   : {result['employee_type']}")
    print_separator()
    print(f"  {'EARNINGS':40} {'AMOUNT':>12}")
    print_separator()
    print(f"  {'Basic Monthly Salary':40} PHP {result['monthly_salary']:>10,.2f}")
    if result['allowances'] > 0:
        print(f"  {'Non-Taxable Allowances':40} PHP {result['allowances']:>10,.2f}")
    print(f"  {'Gross Pay':40} PHP {result['gross_pay']:>10,.2f}")
    print_separator()
    print(f"  {'MANDATORY DEDUCTIONS':40} {'AMOUNT':>12}")
    print_separator()

    if result['employee_type'].lower() == 'private':
        print(f"  {'SSS Contribution':40} PHP {result['sss']:>10,.2f}")
    else:
        print(f"  {'GSIS Contribution':40} PHP {result['gsis']:>10,.2f}")

    print(f"  {'PhilHealth Contribution':40} PHP {result['philhealth']:>10,.2f}")
    print(f"  {'Pag-IBIG (HDMF) Contribution':40} PHP {result['pagibig']:>10,.2f}")
    print(f"  {'Total Mandatory Deductions':40} PHP {result['total_mandatory']:>10,.2f}")
    print_separator()
    print(f"  {'Taxable Income (Monthly)':40} PHP {result['taxable_income']:>10,.2f}")
    print_separator()
    print(f"  {'TAX DEDUCTIONS':40} {'AMOUNT':>12}")
    print_separator()
    print(f"  {'BIR Withholding Tax (TRAIN Law)':40} PHP {result['withholding_tax']:>10,.2f}")
    print_separator()
    print(f"  {'TOTAL DEDUCTIONS':40} PHP {result['total_deductions']:>10,.2f}")
    print_separator("═")
    print(f"  {'NET PAY (Take-Home Pay)':40} PHP {result['net_pay']:>10,.2f}")
    print_separator("═")


def get_float_input(prompt, min_val=0):
    """Get a validated float from the user."""
    while True:
        try:
            value = float(input(prompt).replace(",", ""))
            if value < min_val:
                print(f"  ⚠  Value must be ≥ {min_val}. Try again.")
                continue
            return value
        except ValueError:
            print("  ⚠  Invalid input. Please enter a numeric value.")


def get_choice_input(prompt, valid_choices):
    """Get a validated choice from the user."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"  ⚠  Please enter one of: {', '.join(valid_choices)}")


def run_another():
    """Ask user if they want to compute another payslip."""
    choice = input("\n  Compute another payslip? (yes/no): ").strip().lower()
    return choice in ('yes', 'y')


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN PROGRAM (Procedural Entry Point)
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print_header()
    print("  TRAIN Law Tax Rates | SSS 2025 | PhilHealth 5% | Pag-IBIG")
    print()

    while True:
        print_separator()
        print("  EMPLOYEE INFORMATION")
        print_separator()

        employee_name = input("  Employee Name          : ").strip()
        if not employee_name:
            employee_name = "Unknown"

        employee_type = get_choice_input(
            "  Employee Type (private/government) : ",
            valid_choices=['private', 'government', 'p', 'g']
        )
        # Normalize shorthand
        if employee_type == 'p':
            employee_type = 'private'
        elif employee_type == 'g':
            employee_type = 'government'

        monthly_salary = get_float_input("  Basic Monthly Salary   : PHP ", min_val=0)
        allowances     = get_float_input("  Non-Taxable Allowances : PHP ", min_val=0)

        # Compute
        result = compute_payroll(employee_type, monthly_salary, allowances)

        # Display
        print_payslip(result, employee_name)

        if not run_another():
            print()
            print_separator("═")
            print("  Thank you for using the Philippine Payroll System!")
            print_separator("═")
            break


if __name__ == "__main__":
    main()
