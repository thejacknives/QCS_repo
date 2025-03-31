def tyre_pressure_warning(pressures, target_pressure):
    tyre_averages = []

    for i, tyre_readings in enumerate(pressures):
        print(f"\n--- Processing Tyre {i} ---")

        # Step 1: Input validation
        valid_readings = [p for p in tyre_readings if 0 < p < 100]
        if not valid_readings:
            print(f"[Warning] Tyre {i} has no valid readings, skipping.")
            continue

        # Step 2: Outlier removal
        cleaned = remove_outliers(valid_readings)
        if len(cleaned) == 0:
            print(f"[Warning] Tyre {i} has only outlier readings, skipping.")
            continue

        # Step 3: DMR simulation - compute average in two identical modules
        avg_module_1 = sum(cleaned) / len(cleaned)
        avg_module_2 = sum(cleaned) / len(cleaned)  # Normally this would be another "independent" module
        #UNCOMMENT TO FORCE DMR ERROR
        #if i == 1:
            #avg_module_2 += 1  # simulate fault in module 2


        if abs(avg_module_1 - avg_module_2) > 0.001:
            print(f"[DMR ERROR] Disagreement between modules on Tyre {i}: {avg_module_1} vs {avg_module_2}")
            continue  # DMR detected error, skip this tyre
        else:
            print(f"[DMR OK] Tyre {i} average = {avg_module_1:.2f}")

        # Step 4: Threshold check
        if avg_module_1 < target_pressure:
            tyre_averages.append((i, avg_module_1))

    # Final sorting of low-pressure tyres
    tyre_averages.sort(key=lambda x: x[1])
    return [i for i, _ in tyre_averages]


def remove_outliers(readings, threshold_ratio=0.75):
    if len(readings) < 3:
        return readings  # Not enough data to detect outliers

    filtered = []
    for i, val in enumerate(readings):
        rest = readings[:i] + readings[i+1:]
        rest_avg = sum(rest) / len(rest)

        lower_bound = rest_avg * (1 - threshold_ratio)
        upper_bound = rest_avg * (1 + threshold_ratio) #values higher than 100 are already being ignored.

        if lower_bound <= val <= upper_bound:
            filtered.append(val)
        else:
            print(f"[Outlier Ignored] Value {val} is an outlier compared to average {rest_avg:.2f}")
    return filtered


# Test Case Example from the assignment
print("1-> " ,tyre_pressure_warning([[10], [10], [10], [10]], 5))   #[]
print("2-> " ,tyre_pressure_warning([[10, 10], [10, 10], [10, 10], [10, 10]], 5)) #[]
print("3->" ,tyre_pressure_warning([[10, 10], [30, 30], [20, 20], [40, 40]],  100))  #[0,2,1,3]
print("4->" ,tyre_pressure_warning([[10], [1], [10], [10]], 5))  #[1]
print("5->" ,tyre_pressure_warning([[0, 15], [10, 10], [10, 10], [10, 10]], 8)) #[]  

# Includes invalid and out-of-range values-> input testing
print("6->" ,tyre_pressure_warning([[0, -2, 200], [15, 15], [8, 9]], 10))
# Expected: Tyre 0 ignored, maybe tyres 2 gets flagged

# for outlier detection. ->ignoring 100, etc.
print("7->" ,tyre_pressure_warning([
    [10, 10, 10, 1],     # 1000 is clearly an outlier now
    [30, 30, 30],
    [0, 30, 10, 12],       # 0 ignored, 100 might get flagged
    [10, 11, 12]
], 25))

