import time
import statistics

def filter_temperature(sensor_readings, threshold=5):
    """
    Outlier detection for a zone's temperature sensor readings.
    
    If sensor_readings is a list, compute the median and then average only the values
    that are within `threshold` degrees of the median. If no reading passes the filter,
    return the median.
    
    If sensor_readings is a single number, return it.
    """
    if isinstance(sensor_readings, list):
        if len(sensor_readings) == 1:
            return sensor_readings[0]
        med = statistics.median(sensor_readings)
        filtered = [t for t in sensor_readings if abs(t - med) <= threshold]
        return sum(filtered) / len(filtered) if filtered else med
    else:
        return sensor_readings

def climate_control_ft(desired_temp, error, temps, fans):
    """
    Fault-tolerant primary function for FR6 (Climate control).
    
    Implements:
      - Consistency Checks: Verifies each temperature and fan duty is within acceptable ranges.
      - Outlier Detection: For each zone, if multiple sensor readings are provided (as a list),
        computes a filtered (representative) temperature.
    
    For each zone:
      - If the (filtered) temperature is within [desired_temp - error, desired_temp + error],
        no adjustment is made.
      - If too low, fan duty is increased by 20% if the zone’s average is 0%, otherwise by 10%.
      - If too high, fan duty is decreased similarly.
    
    Parameters:
      desired_temp (float): Desired temperature in Celsius.
      error (float): Allowable error margin.
      temps (list): For each zone, either a single temperature (float) or a list of sensor readings.
      fans (list of list of int): Current fan duty cycles per zone (each value 0 to 100).
      
    Returns:
      list of list of int: New fan duty cycles for each zone.
    """
    # Consistency checks for temperatures:
    for t in temps:
        if isinstance(t, list):
            for reading in t:
                assert isinstance(reading, (int, float)), "Temperature must be numeric"
                assert -40 <= reading <= 60, f"Temperature {reading} out of expected range (-40, 60)"
        else:
            assert isinstance(t, (int, float)), "Temperature must be numeric"
            assert -40 <= t <= 60, f"Temperature {t} out of expected range (-40, 60)"
    
    # Consistency checks for fan duty cycles:
    for zone in fans:
        for duty in zone:
            assert isinstance(duty, (int, float)), "Fan duty must be numeric"
            assert 0 <= duty <= 100, f"Fan duty {duty} out of range (0, 100)"
    
    lower = desired_temp - error
    upper = desired_temp + error
    new_fans = []
    
    for temp, zone in zip(temps, fans):
        # Apply outlier detection: if temp is a list, filter it; otherwise, use it directly.
        filtered_temp = filter_temperature(temp)
        
        # Compute average fan duty for the zone.
        avg = sum(zone) / len(zone)
        
        # If temperature is within the desired range, keep fan duties unchanged.
        if lower <= filtered_temp <= upper:
            new_fans.append(zone.copy())
            continue
        
        # Determine adjustment delta: 20% if average is 0, else 10%.
        delta = 20 if avg == 0 else 10
        
        if filtered_temp < lower:
            adjusted = [min(100, f + delta) for f in zone]
        else:  # filtered_temp > upper
            adjusted = [max(0, f - delta) for f in zone]
        new_fans.append(adjusted)
    
    return new_fans

def majority_vote(replica_outputs):
    """
    Perform majority voting over a list of replicated outputs.
    
    Each output is a list of zones (each zone is a list of fan duty values). Voting is done
    element-wise: for each zone and each fan index, if at least two replicas agree, that value is chosen.
    
    Returns:
      list of list of int: The final voted output.
    """
    num_zones = len(replica_outputs[0])
    voted_output = []
    for zone_index in range(num_zones):
        # Collect outputs for the current zone from all replicas.
        zone_votes = [replica[zone_index] for replica in replica_outputs]
        num_fans = len(zone_votes[0])
        voted_zone = []
        for fan_index in range(num_fans):
            votes = [zone[fan_index] for zone in zone_votes]
            if votes[0] == votes[1] or votes[0] == votes[2]:
                voted_value = votes[0]
            elif votes[1] == votes[2]:
                voted_value = votes[1]
            else:
                voted_value = votes[0]  # fallback if all differ
            voted_zone.append(voted_value)
        voted_output.append(voted_zone)
    return voted_output

def climate_control_rep(desired_temp, error, temps, fans, num_replicas=3):
    """
    Fault-tolerant climate control using replication with majority voting (TMR).
    
    This function replicates the primary function (climate_control_ft) num_replicas times and then
    applies majority voting on the outputs to mask transient faults.
    
    Parameters:
      desired_temp (float): Desired temperature in Celsius.
      error (float): Allowable error margin.
      temps (list): For each zone, either a single temperature reading or a list of readings.
      fans (list of list of int): Current fan duty cycles per zone.
      num_replicas (int): Number of replications (default is 3 for TMR).
    
    Returns:
      list of list of int: The final, voted fan duty cycles.
    """
    replica_outputs = []
    for _ in range(num_replicas):
        replica_outputs.append(climate_control_ft(desired_temp, error, temps, fans))
    return majority_vote(replica_outputs)


# --- Test Harness ---

if __name__ == "__main__":
    # Test inputs: using single readings per zone and one example with multiple sensor values.
    test_inputs = [
        # TC1: Single sensor reading per zone.
        (25, 3, [23], [[0, 0, 0]]),
        # TC2: Two zones with single sensor readings.
        (25, 3, [20, 18], [[10, 10], [5, 5]]),
        # TC3: Two zones; one with an outlier reading provided as a list.
        (25, 3, [[20, 50, 20], 18], [[10, 0], [0, 0]]),
        # TC4: Two zones; temperatures above the upper bound.
        (15, 3, [20, 18], [[10, 0], [0, 0]]),
        # TC5: Two zones; one with high fan duty adjustments.
        (30, 3, [20, 18], [[95, 70], [100, 0]])
    ]
    
    # Expected outputs for the primary function (when applied without replication):
    expected_primary_outputs = [
        [[0, 0, 0]],                            # TC1: 23 is within [22, 28]
        [[20, 20], [15, 15]],                    # TC2: 20 and 18 are below 22 → increase
        [[20, 10], [20, 20]],                    # TC3: For first zone, outlier detection filters [20,50,20] to ~20
        [[0, 0], [0, 0]],                        # TC4: Temperatures above range → decrease
        [[100, 80], [100, 10]]                    # TC5: Adjustments based on computed averages
    ]
    
    #print("Testing primary fault-tolerant function with outlier detection (climate_control_ft):")
    for idx, (d, e, temps, fans) in enumerate(test_inputs, start=1):
        try:
            result = climate_control_ft(d, e, temps, fans)
    #        print(f"TC{idx}: {result}")
        except Exception as err:
            print(f"TC{idx}: Error: {err}")
    
    #   print("\nTesting replication with majority voting (climate_control_rep):")
    for idx, (d, e, temps, fans) in enumerate(test_inputs, start=1):
        try:
            result = climate_control_rep(d, e, temps, fans)
            print(f"TC{idx}: {result}")
        except Exception as err:
            print(f"TC{idx}: Error: {err}")
