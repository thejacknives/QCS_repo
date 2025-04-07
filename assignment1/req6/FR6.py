def climate_control(desired_temp, error, temps, fans):
    """
    Baseline implementation of FR6 (Climate Control).

    For each zone:
      - If the temperature is within the desired range [desired_temp - error, desired_temp + error],
        no adjustment is made.
      - If the temperature is too low, the fan duty cycles are increased.
      - If the temperature is too high, the fan duty cycles are decreased.
      - The adjustment is:
            • 20% if the average fan duty of the zone is 0%
            • Otherwise, 10%

    Parameters:
      desired_temp (float): Desired temperature in Celsius.
      error (float): Allowable error margin.
      temps (list of float): Temperature readings from each zone.
      fans (list of list of int): Current fan duty cycles per zone (each value between 0 and 100).

    Returns:
      list of list of int: New fan duty cycles for each zone.
    """
    lower = desired_temp - error
    upper = desired_temp + error
    new_fans = []

    for temp, zone in zip(temps, fans):
        # Calculate the average fan duty for the zone.
        avg = sum(zone) / len(zone)

        # If temperature is within the acceptable range, keep the fan duties unchanged.
        if lower <= temp <= upper:
            new_fans.append(zone.copy())
            continue

        # Determine adjustment delta: 20% if the average is 0, else 10%.
        delta = 20 if avg == 0 else 10

        if temp < lower:
            adjusted = [min(100, f + delta) for f in zone]
        else:  # temp > upper
            adjusted = [max(0, f - delta) for f in zone]
        new_fans.append(adjusted)

    return new_fans


# --- Test Harness for the Baseline Version ---

if __name__ == "__main__":
    test_inputs = [
        (25, 3, [23], [[0, 0, 0]]),                         # TC1
        (25, 3, [20, 18], [[10, 10], [5, 5]]),               # TC2
        (25, 3, [20, 18], [[10, 0], [0, 0]]),                # TC3
        (15, 3, [20, 18], [[10, 0], [0, 0]]),                # TC4
        (30, 3, [20, 18], [[95, 70], [100, 0]])              # TC5
    ]

    expected_outputs = [
        [[0, 0, 0]],                                        # Expected for TC1
        [[20, 20], [15, 15]],                                # Expected for TC2
        [[20, 10], [20, 20]],                                # Expected for TC3
        [[0, 0], [0, 0]],                                    # Expected for TC4
        [[100, 80], [100, 10]]                               # Expected for TC5
    ]

    for idx, ((d, e, temps, fans), expected) in enumerate(zip(test_inputs, expected_outputs), start=1):
        result = climate_control(d, e, temps, fans)
        #status = "✅" if result == expected else "❌"
        #print(f"TC{idx}: got {result} — expected {expected} {status}")
        print(result)
