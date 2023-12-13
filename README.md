# PID-Genetic-Optimizer
_____
## Overview

The PID Genetic Optimizer is a tool designed to find optimal Proportional-Integral-Derivative (PID) controller values for a given system. The idea behind this code is to use a genetic algorithm to generate a population of PID parameters and iteratively refine them based on the performance metric of the system.

This optimizer involves human interaction to select the best-performing PID values among the generated population. The performance metric uses a cost function to measure the performance using time reference, where the algorithm chooses the parameters resulting in the lowest time to meet the desired system behavior.

The genetic algorithm employed in this optimizer uses arithmetic crossover as the primary genetic operator.

## How It Works

The PID Genetic Optimizer follows these steps:

```` mermaid

flowchart TD

id1([Initialization]) --> id2([Genetic Operations]) --> id3([Evaluation]) --> id4([Selection])

id4 ---> id2

````

1. **Initialization:** It begins by generating an initial population of PID parameters.

2. **Genetic Operations:** The selected parameters undergo genetic operations like arithmetic crossover to produce a new generation of PID parameters.

3. **Evaluation:** The system's performance is evaluated using each set of parameters. The metric used here is time-based, selecting the parameters resulting in the lowest cost (time) for the system to achieve the desired state.

4. **Selection:** The best-performing PID parameters are selected based on the evaluation metric. A human-in-the-loop interaction occurs to choose the best among these parameters.

5. **Iteration:** Steps 2-4 are repeated for a specified number of iterations or until a stopping criterion is met.

## Initial Parameters by Ziegler-Nichols Method

The initial parameters for the PID Genetic Optimizer are generated using the Ziegler-Nichols method, a widely used technique for tuning PID controllers. The Ziegler-Nichols method involves conducting experiments to find the ultimate gain ($K_u$) and the ultimate period ($T_u$) of a system.

In our system, the integral gain ($K_I$) has no weight, and thus, it is set to 0. This is due to the specific characteristics of the controlled process and is reflected in the optimizer's configuration.

| Control Type           | $K_P$    | $T_i$      | $T_d$       | $K_I$             | $K_D$               |
|------------------------|-------|---------|----------|----------------|------------------|
| P                      | 0.5 $K_u$  | –       | –        | -          | –                |
| PI                     | 0.45 $K_u$  | 0.83 $T_u$       | –        | 0.54 $\frac{K_u}{T_u}$         | -       |
| PD                     | 0.8 $K_u$   | –       | 0.125 $T_u$        | -          | 0.10 $K_uT_u$                |
| Classic PID       | 0.6 $K_u$   | 0.5 $T_u$       | 0.125 $T_u$        | 1.2 $\frac{K_u}{T_u}$          | 0.075 $K_uT_u$        |
| Pessen Integral Rule| 0.7 $K_u$   | 0.4 $T_u$       | 0.15 $T_u$        | 1.75 $\frac{K_u}{T_u}$          | 0.105 $K_uT_u$         |
| Some Overshoot    | 0.33 $K_u$ | 0.50 $T_u$    | 0.33 $T_u$   | 0.66 $\frac{K_u}{T_u}$         | 0.11 $K_uT_u$       |
| No Overshoot       | 0.20 $K_u$  | 0.50 $T_u$    | 0.33 $T_u$   | 0.40 $\frac{K_u}{T_u}$      | 0.066 $K_uT_u$      |

For a PD controller, the initial proportional gain ($K_P$) is then set to 0.8 times $K_u$ and the initial derivative gain ($K_D$) is set to 0.10 times $K_u$ times $T_u$.

In our case, the experimentally determined values are: 
- $K_u = 0.0175$
- $T_u = \frac{1}{8}$ seconds

This results in the following initial values:
- $K_P=0.0175\times0.8=0.014$
- $K_D=0.10\times0.0175\times0.125=0.0002$

Here is an example code that generates the other initial chromosomes based on the values generated using the Ziegler-Nichols method. The code can be found [here](https://github.com/MAMV3x3/PID-Genetic-Optimizer/blob/main/initial_parameters.py).

## Genetic Algorithm and Arithmetic Crossover

The genetic algorithm used in this optimizer involves arithmetic crossover as a key genetic operator. Arithmetic crossover blends the values of parameters from two selected PID sets to create offspring that inherit characteristics from both parents.

In case of real-value encoding, to implement arithmetic crossover. We can use a arithmetic crossover operator linearly to combines the two parent chromosomes. In an arithmetic crossover, randomly two chromosomes are selected for crossover, and by a linear combination of these chromosomes, two off springs are produced. This linear combination is as per the following computation:

```python
alpha = random.uniform(0, 1)
Child = alpha * P1gene + (1-alpha) * P2gene  
```

## Requirements

- Python 3.X: The codebase requires a version of Python 3.0+ Make sure you have Python installed. You can download Python from [here](https://www.python.org/downloads/).

- Matplotlib: The `matplotlib` library is used for data visualization within this project. You can install it via pip:

```bash
$ pip install matplotlib
```

## Usage  

To use the PID Genetic Optimizer:

1. **Clone the Repository:** `git clone https://github.com/MAMV3x3/PID-Genetic-Optimizer`

2. **Run the Code:** Execute the main script, following the instructions.

The console will prompt the following question

```bash
  Do you want to load from a file? (y/n):
```

This is only when an iteration has already been done to renew the progress from the last iteration

This is the following prompt it ask for a manual input for the first generation of PID values, otherwise it will initialize random values

```bash
  Do you want to input custom values? (y/n):
```

After this, values will be generated and a human must evaluate them, recording each time performance in the console and after the generation is completed, it will ask to save the best value in a file just before proceeding to the next generation. The stop criteria has to be at the human consideration at the moment the ideal performance is reached.
## Results

The optimization process was run for multiple iterations, and here are the results for the best chromosomes over generations:

| Iteration | Gen | Number | KP                   | KD                   | Lap Time |
|-----------|-----|--------|----------------------|----------------------|----------|
| 1         | 1   | 5      | 0.014586226564698124 | 0.06521582373854175  | 3.85     |
| 2         | 1   | 5      | 0.014586226564698124 | 0.06521582373854175  | 3.85     |
| 3         | 3   | 18     | 0.014404903617277962 | 0.10158877009982219  | 3.74     |
| 4         | 3   | 18     | 0.014404903617277962 | 0.10158877009982219  | 3.74     |
| 5         | 5   | 23     | 0.012474477296694935 | 0.29396664154337565  | 3.69     |
| 6         | 5   | 23     | 0.012474477296694935 | 0.29396664154337565  | 3.69     |
| 7         | 7   | 41     | 0.012819959187179835 | 0.20226760794961973  | 3.61     |
| 8         | 8   | 50     | 0.012819959187179835 | 0.24676955949997498  | 3.58     |
| 9         | 10  | 67     | 0.01257733001537879  | 0.2797784764167482   | 3.54     |
| 10        | 10  | 67     | 0.01257733001537879  | 0.2797784764167482   | 3.54     |
| 11        | 11  | 74     | 0.013287624538492666 | 0.260206824009848    | 3.49     |

### Performance Plots

#### Lap Time Evolution Over Generations

![Time](https://github.com/MAMV3x3/PID-Genetic-Optimizer/assets/84588180/ffa40408-1695-4e9a-8182-37ae29fe6dc8)

#### Parameter Evolution Over Generations

![Constants](https://github.com/MAMV3x3/PID-Genetic-Optimizer/assets/84588180/6d4b2b0c-57e8-49ac-a865-6c0629ab8a18)

The code to generate the plots is available [here](https://github.com/MAMV3x3/PID-Genetic-Optimizer/blob/main/plotting.py).
### Comparison

Compare the last iteration's values with the expert-set manual values of KP=0.013 and KD=0.26.

- **Manually set KP**: 0.013
- **Manually set KD**: 0.26

- **Last iteration KP**: 0.013287624538492666
- **Last iteration KD**: 0.260206824009848

## References

1. Performance of Arithmetic Crossover and Heuristic Crossover in Genetic Algorithm Based on Alpha Parameter: [Paper Link](https://www.iosrjournals.org/iosr-jce/papers/Vol19-issue5/Version-1/F1905013136.pdf)
2. Ziegler–Nichols Method: [Wikipedia](https://en.wikipedia.org/wiki/Ziegler%E2%80%93Nichols_method)
3. Genetic Algorithms: [Kramer, O. (2017). Genetic Algorithms. Springer International Publishing.](https://link.springer.com/book/10.1007/978-3-319-52156-5)
4. Genetic Algorithms in Optimization: [Goldberg, D. E. (1989). Genetic Algorithms in Search, Optimization, and Machine Learning.](https://dl.acm.org/doi/10.5555/534133)
