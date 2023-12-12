import numpy as np

def generate_parameters(initial_kp, initial_kd, num_sets, deviation):
    parameters = []
    for _ in range(num_sets):
        kp = np.random.normal(initial_kp, deviation)
        kd = np.random.normal(initial_kd, deviation)
        parameters.append((kp, kd))
    return parameters

# Example usage
initial_kp = 0.014
initial_kd = 0.0002
num_sets = 4
deviation = 0.1

# Generate parameters and take the absolute value of each parameter
generated_parameters = generate_parameters(initial_kp, initial_kd, num_sets, deviation)
generated_parameters = [(abs(kp), abs(kd)) for kp, kd in generated_parameters]
print("Original Parameters: KP={}, KD={}".format(initial_kp, initial_kd))
print("Generated Parameters:")
for i, (kp, kd) in enumerate(generated_parameters, start=1):
    print(f"Set {i}: KP={kp}, KD={kd}")
