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

    plt.plot(iterations, lap_times, marker='o', label='Lap Time', color='limegreen')

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

    # Create a figure and primary axis
    fig, ax1 = plt.subplots()

    # Plot KD values on the primary axis
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('KD', color='deeppink')
    kd_line, = ax1.plot(iterations, kd_values, marker='o', color='deeppink', label='KD')
    ax1.tick_params(axis='y', labelcolor='deeppink')

    # Create a secondary y-axis
    ax2 = ax1.twinx()

    # Plot KP values on the secondary axis
    ax2.set_ylabel('KP', color='mediumblue')
    kp_line, = ax2.plot(iterations, kp_values, marker='o', color='mediumblue', label='KP')
    ax2.tick_params(axis='y', labelcolor='mediumblue')

    # Add dotted lines for ideal KP and KD if provided
    if ideal_kp is not None:
        ideal_kp_line = ax2.axhline(y=ideal_kp, linestyle='--', color='cornflowerblue', label='Ideal KP')

    if ideal_kd is not None:
        ideal_kd_line = ax1.axhline(y=ideal_kd, linestyle='--', color='pink', label='Ideal KD')

    # Display the plot with explicit legend handles and labels
    plt.title('Parameter Evolution Over Generations')
    plt.legend(handles=[kd_line, kp_line, ideal_kd_line, ideal_kp_line],
               labels=['KD', 'KP', 'Ideal KD', 'Ideal KP'])
    plt.show()

ideal_kp = 0.013
ideal_kd = 0.26

plot_lap_time_evolution('best_chromosomes.jsonl')
plot_parameter_evolution('best_chromosomes.jsonl', ideal_kp, ideal_kd)
