def tyre_pressure_warning(pressures, target_pressure):
    tyre_averages = []

    for i, tyre_readings in enumerate(pressures):
        # Filter out sensor malfunction readings (0 PSI) also no negative pressure readings
        valid_readings = [p for p in tyre_readings if p > 0]

        if not valid_readings:
            continue  # No valid readings, skip tyre

        average = sum(valid_readings) / len(valid_readings)

        if average < target_pressure:
            tyre_averages.append((i, average))

    # Sort tyres by average pressure (ascending)
    tyre_averages.sort(key=lambda x: x[1])

    # Return only the indices
    return [i for i, _ in tyre_averages]


# Test Case Example from the assignment
print(tyre_pressure_warning([[10], [10], [10], [10]], 5))   #[]
print(tyre_pressure_warning([[10, 10], [10, 10], [10, 10], [10, 10]], 5)) #[]
print(tyre_pressure_warning([[10, 10], [30, 30], [20, 20], [40, 40]],  100))  #[0,2,1,3]
print(tyre_pressure_warning([[10], [1], [10], [10]], 5))  #[1]
print(tyre_pressure_warning([[0, 15], [10, 10], [10, 10], [10, 10]], 8)) #[]  