import json
import matplotlib.pyplot as plt

def plot_lap_time_evolution(filename):
    iterations = []
    lap_times = []

    with open(filename, 'r') as file:
        for i, line in enumerate(file, start=1):
            data = json.loads(line)
            iterations.append(i)
            lap_times.append(data['lap_time'])

    plt.plot(iterations, lap_times, marker='o', label='Lap Time')
    
    plt.title('Lap Time Evolution Over Generations')
    plt.xlabel('Iteration')
    plt.ylabel('Lap Time')
    plt.legend()
    plt.show()

def plot_parameter_evolution(filename, ideal_kp=None, ideal_kd=None):
    iterations = []
    kp_values = []
    kd_values = []

    with open(filename, 'r') as file:
        for i, line in enumerate(file, start=1):
            data = json.loads(line)
            iterations.append(i)
            kp_values.append(data['kp'])
            kd_values.append(data['kd'])

    plt.plot(iterations, kp_values, label='KP', marker='o', color='mediumblue')
    plt.plot(iterations, kd_values, label='KD', marker='o', color='deeppink')
    
    # Add dotted lines for ideal KP and KD if provided
    if ideal_kp is not None:
        plt.axhline(y=ideal_kp, linestyle='--', color='cornflowerblue', label='Ideal KP')

    if ideal_kd is not None:
        plt.axhline(y=ideal_kd, linestyle='--', color='pink', label='Ideal KD')

    plt.title('Parameter Evolution Over Generations')
    plt.xlabel('Iteration')
    plt.ylabel('Parameter Value')
    plt.legend()
    plt.show()

ideal_kp = 0.013
ideal_kd = 0.26 

plot_lap_time_evolution('best_chromosomes.jsonl')
plot_parameter_evolution('best_chromosomes.jsonl', ideal_kp, ideal_kd)
