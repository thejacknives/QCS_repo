
def tyre_pressure_warning(pressures, target_pressure):
    tyre_averages = []

    for i, tyre_readings in enumerate(pressures):
        # Filter out invalid readings (0, negative, or too large)-> !!!! input validation / filtering
        valid_readings = [p for p in tyre_readings if 0 < p < 100 ]

        #warning if tire doesnt have ANY valid readings i.e average cant be calculated.
        if not valid_readings:
            print(f"[Warning] Tyre {i} has no valid readings, skipping.")
            continue
        
        # Step 2: Remove outliers
        cleaned = remove_outliers(valid_readings)
        if len(cleaned) == 0:
            #unlikely to happen, but if all readings are outliers, skip
            print(f"[Warning] Tyre {i} has only outlier readings, skipping.")
            continue

        average = sum(valid_readings) / len(valid_readings)

        if average < target_pressure:
            tyre_averages.append((i, average))

    # Sort by average pressure
    tyre_averages.sort(key=lambda x: x[1])

    return [i for i, _ in tyre_averages]


def remove_outliers(readings, threshold_ratio=0.5):
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

