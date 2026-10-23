import subprocess, sys

test_input = "Juan dela Cruz\nprivate\n30000\n1500\nno\n"
result = subprocess.run(
    [sys.executable, r"c:\Users\User\Yangmin\MCO 1 (Ventures)\payroll_python\payroll_system.py"],
    input=test_input, capture_output=True, text=True, timeout=30
)
print("STDOUT:\n", result.stdout)
if result.stderr:
    print("STDERR:\n", result.stderr)
