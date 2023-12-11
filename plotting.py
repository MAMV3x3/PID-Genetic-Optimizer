import json
import matplotlib.pyplot as plt

def plot_lap_time_evolution(filename):
    generations = []
    lap_times = []

    with open(filename, 'r') as file:
        for line in file:
            data = json.loads(line)
            generations.append(data['gen'])
            lap_times.append(data['lap_time'])

    plt.plot(generations, lap_times, marker='o')
    plt.title('Lap Time Evolution Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Lap Time')
    plt.show()

def plot_parameter_evolution(filename):
    generations = []
    kp_values = []
    ki_values = []
    kd_values = []

    with open(filename, 'r') as file:
        for line in file:
            data = json.loads(line)
            generations.append(data['gen'])
            kp_values.append(data['kp'])
            ki_values.append(data['ki'])
            kd_values.append(data['kd'])

    plt.plot(generations, kp_values, label='KP', marker='o')
    plt.plot(generations, ki_values, label='KI', marker='o')
    plt.plot(generations, kd_values, label='KD', marker='o')
    plt.title('Parameter Evolution Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Parameter Value')
    plt.legend()
    plt.show()

# Add these function calls at the end of your script
plot_lap_time_evolution('best_chromosomes.jsonl')
plot_parameter_evolution('best_chromosomes.jsonl')
