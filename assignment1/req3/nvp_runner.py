# nvp_runner.py
from req3_Fault import tyre_pressure_warning as fault_tolerance_version
from Re3_tomas_tavares import tyre_pressure as n_version2

# Same test cases for both versions
test_cases = [
    ([[10], [10], [10], [10]], 5),
    ([[10, 10], [10, 10], [10, 10], [10, 10]], 5),
    ([[10, 10], [30, 30], [20, 20], [40, 40]], 100),
    ([[10], [1], [10], [10]], 5),
    ([[0, 15], [10, 10], [10, 10], [10, 10]], 8),
    ([[0, -2, 200], [15, 15], [8, 9]], 10),
    ([[10, 10, 10, 1], [30, 30, 30], [0, 30, 10, 12], [10, 11, 12]], 25)
]

# Separate inputs for each
pressures = [case[0] for case in test_cases]
targets = [case[1] for case in test_cases]

# Run fault-tolerant version
ft_outputs = []
for i in range(len(test_cases)):
    result = fault_tolerance_version(pressures[i], targets[i])
    ft_outputs.append(result)

# Run v2 version
v2_outputs = n_version2(pressures, targets)

# Save outputs
with open("ft_output.txt", "w") as f:
    for i, out in enumerate(ft_outputs):
        f.write(f"Test Case {i+1}: {out}\n")

with open("v2_output.txt", "w") as f:
    for i, out in enumerate(v2_outputs):
        f.write(f"Test Case {i+1}: {out}\n")

# Compare and print results
print("\n--- N-Version Comparator ---")
for i, (out1, out2) in enumerate(zip(ft_outputs, v2_outputs)):
    attempts = 1
    while out1 != out2 and attempts <= 3:
        print(f"[WARNING] Output mismatch in Test Case {i+1} (Attempt {attempts})")
        print(f"  Fault-Tolerant: {out1}")
        print(f"  V2 Version:     {out2}")
        if attempts == 3:
            print(f"[ERROR] Persistent mismatch in Test Case {i+1} after 3 attempts.")
            break
        # Re-run the test case
        out1 = fault_tolerance_version(pressures[i], targets[i])
        out2 = n_version2([pressures[i]], [targets[i]])[0]
        attempts += 1
    if out1 == out2:
        print(f"[OK] Test Case {i+1} → Output: {out1}")