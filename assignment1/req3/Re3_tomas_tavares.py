from cv2 import sort


test_cases = [
    ([[10], [10], [10], [10]], 5), 
    ([[10, 10], [10, 10], [10, 10], [10, 10]], 5),  
    ([[10, 10], [30, 30], [20, 20], [40, 40]], 100),  
    ([[10], [1], [10], [10]], 5),  
    ([[0,15], [10, 10], [10, 10], [10, 10]], 8),  
]

##parse test cases
pressures = [case[0] for case in test_cases]
target = [case[1] for case in test_cases]

#print (pressures)
#print (target)

def tyre_pressure(pressures, target_pressures):
    means = mean_pressures(pressures)
    tests_output = []
    
    for idx, case_means in enumerate(means):
        underpressure = []
        for tyre_idx, avg in enumerate(case_means):
            # Skip tyres marked as invalid (None)
            if avg is None:
                continue
            # Check if below target pressure
            if avg < target_pressures[idx]:
                underpressure.append((tyre_idx, avg))
        
        # Sort by ascending average pressure
        underpressure.sort(key=lambda x: x[1])
        # Extract tyre indices
        sorted_tyres = [x[0] for x in underpressure]
        tests_output.append(sorted_tyres)
        # Print warnings for each tyre
        #for tyre_idx, avg in underpressure:
            #print(f"Warning: tyre pressure in TC{idx + 1} is too low in tyre {tyre_idx} (average: {avg}) target: {target_pressures[idx]})")
    print("tests output: " ,tests_output)
    return tests_output

def mean_pressures(pressures):
    means = []
    for case in pressures:
        tyre_means = []
        for tyre in case:
            # Remove 0 PSI readings (hardware failure)
            valid_readings = [psi for psi in tyre if psi != 0]
            
            # If all readings are 0 or there are no reading, mark tyre as none
            if len(valid_readings) == 0:
                tyre_means.append(None)  
            else:
                avg = sum(valid_readings) / len(valid_readings)
                tyre_means.append(avg)
        means.append(tyre_means)
    return means

tyre_pressure(pressures, target)