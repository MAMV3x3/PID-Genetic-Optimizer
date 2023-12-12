import random
import copy
import json

class Chromosome:
    chromosome_count = 0

    def __init__(self, gen, kp, kd):
        Chromosome.chromosome_count += 1
        self.gen = gen
        self.number = Chromosome.chromosome_count
        self.kp = kp
        self.kd = kd
        self.lap_time = None

    def mutate(self, mutation_rate):
        mutation_range_kp = 0.1
        mutation_range_kd = 0.3

        if random.random() < mutation_rate:
            self.kp = max(0, min(1, self.kp + random.uniform(-mutation_range_kp, mutation_range_kp)))

        if random.random() < mutation_rate:
            self.kd = max(0, min(1, self.kd + random.uniform(-mutation_range_kd, mutation_range_kd)))

    def clone(self):
        return copy.deepcopy(self)

    def to_dict(self):
        return {
            'gen': self.gen,
            'number': self.number,
            'kp': self.kp,
            'kd': self.kd,
            'lap_time': self.lap_time
        }

    @classmethod
    def from_dict(cls, data):
        chromosome = cls(data['gen'], data['kp'], data['kd'])
        chromosome.number = data['number']
        chromosome.lap_time = data['lap_time']
        return chromosome

class Population:
    def __init__(self, size):
        self.size = size
        self.chromosomes = [Chromosome(1, random.uniform(0, 1), random.uniform(0, 1)) for _ in range(size)]

    def to_dict(self):
        return {'chromosomes': [chromosome.to_dict() for chromosome in self.chromosomes]}

    @classmethod
    def from_dict(cls, data):
        population = cls(len(data['chromosomes']))
        population.chromosomes = [Chromosome.from_dict(chromosome_data) for chromosome_data in data['chromosomes']]
        return population

def report_lap_time(chromosome):
    while True:
        try:
            lap_time = float(input(f"Enter lap time for Chromosome {chromosome.number} (Gen {chromosome.gen}): "))
            chromosome.lap_time = lap_time
            print(f"Lap time for Chromosome {chromosome.number}: {lap_time}")
            break
        except ValueError:
            print("Invalid input. Please enter a valid lap time.")

def display_chromosomes(population):
    print("\nChromosomes:")
    for chromosome in population.chromosomes:
        print(f"Chromosome {chromosome.number} (Gen {chromosome.gen}): KP={chromosome.kp}, KD={chromosome.kd}")

def crossover(parent1, parent2):
    # Perform a simple arithmetic crossover for both KP and KD
    alpha_kp = random.uniform(0, 1)
    alpha_kd = random.uniform(0, 1)
    
    kp = alpha_kp * parent1.kp + (1 - alpha_kp) * parent2.kp
    kd = alpha_kd * parent1.kd + (1 - alpha_kd) * parent2.kd
    
    return Chromosome(gen=parent1.gen, kp=kp, kd=kd)

def generate_next_generation(population, mutation_rate):
    sorted_chromosomes = sorted(population.chromosomes, key=lambda x: x.lap_time)
    best_chromosome = sorted_chromosomes[0]

    print("\nBest Chromosome (Gen {}): KP={}, KD={}, Lap Time={}".format(
        best_chromosome.gen, best_chromosome.kp, best_chromosome.kd, best_chromosome.lap_time))

    new_chromosomes = [best_chromosome.clone()]

    for i in range(1, population.size):
        # Apply crossover to generate new chromosomes
        parent1 = best_chromosome
        parent2 = random.choice(sorted_chromosomes[1:])  # Choose from the rest of the population
        new_chromosome = crossover(parent1, parent2)

        # Update the generation number based on the biggest generation number of all chromosomes
        new_chromosome.gen = max(parent1.gen, parent2.gen) + 1

        # Apply mutation to the new chromosome
        new_chromosome.mutate(mutation_rate)

        new_chromosomes.append(new_chromosome)

    new_population = Population(population.size)
    new_population.chromosomes = new_chromosomes

    return new_population

def save_population(population, filename, generation):
    data = population.to_dict()
    data['generation'] = generation
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_population(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    population = Population(len(data['chromosomes']))
    population.chromosomes = [Chromosome.from_dict(chromosome_data) for chromosome_data in data['chromosomes']]
    return population, data.get('generation', 1)

def save_best_chromosomes(best_chromosomes, filename):
    with open(filename, 'a') as file:
        for chromosome in best_chromosomes:
            json_str = json.dumps(chromosome.to_dict())
            file.write(json_str + '\n')

def main():
    population_size = 5
    generations = 1000
    mutation_rate = 0.35

    load_from_file = input("Do you want to load from a file? (y/n): ").lower() == 'y'
    if load_from_file:
        filename = input("Enter filename to load: ")
        population, current_generation = load_population(filename)
    else:
        population = Population(population_size)
        current_generation = 1

    custom_values = input("Do you want to input custom values? (y/n): ").lower() == 'y'
    if custom_values:
        for chromosome in population.chromosomes:
            chromosome.kp = float(input(f"Enter custom KP for Chromosome {chromosome.number}: "))
            chromosome.kd = float(input(f"Enter custom KD for Chromosome {chromosome.number}: "))

    for gen in range(current_generation, generations + 1):
        print(f"\nGeneration {gen}")

        display_chromosomes(population)

        for chromosome in population.chromosomes:
            report_lap_time(chromosome)

        save_to_file = input("Do you want to save to a file? (y/n): ").lower() == 'y'
        if save_to_file:
            filename = input("Enter filename to save: ")
            save_population(population, filename, gen)

        best_chromosomes = sorted(population.chromosomes, key=lambda x: x.lap_time)[:1]
        save_best_chromosomes(best_chromosomes, 'best_chromosomes.jsonl')

        population = generate_next_generation(population, mutation_rate)

    print("\nEvolution complete.")

if __name__ == "__main__":
    main()
