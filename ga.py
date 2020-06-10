import json
import random
import matplotlib.pyplot as plt


def checkIfEligible(i, j):
  '''
    checks if member ith can perform task j
  '''
  for skill in range(ns):
    # if task needs skill
    if task_skills[j][skill]:
      # and team member doesnt have that skill
      if not team_skills[i][skill]:
        return False
  
  return True


def create_individual():
  '''
    returns a random individual
  '''
  return [random.randint(0, m) for _ in range(n)]


def fitness(individual):
  fitness = 0
  weights = [0]*m

  for index, val in enumerate(individual):
    # if gene value is valid
    if val > 0 and val <= m and canPerformTask[val-1][index]:
      weights[val-1] += time[val-1][index]
      fitness += profit[index]

    # report invalid chromosome - 0 fitness
    elif val < 0 or val > m:
      return 0

  # check for invalid chromosome
  for val in weights:
    if val > t:
      return 0

  return fitness


def crossover(parent_1, parent_2):
  '''
    applies two point crossover
    to generate offsprings
  '''

  # select two points for crossover
  index1 = random.randrange(1, n)
  index2 = random.randrange(1, n)
  index1, index2 = min(index1, index2), max(index1, index2)

  # generate offsprings
  child_1 = parent_1[:index1] + parent_2[index1:index2] + parent_1[index2:]
  child_2 = parent_2[:index1] + parent_1[index1:index2] + parent_2[index2:]

  return child_1, child_2


def mutate(individual):
  '''
    applies random resetting method 
    to mutate an individual
  '''

  # mutate each locus with given probability
  for index in range(n):
    r = random.random()

    if r < mutation_probability:
      individual[index] = random.randint(0, m)
  
  return (individual)


def selection(population):
  '''
    applies Tournament selection method
    to select parent
  '''

  # select two random chromosomes
  index1 = random.randrange(population_size)
  index2 = random.randrange(population_size)

  # calculate their fitness
  fitness1 = fitness(population[index1])
  fitness2 = fitness(population[index2])

  # threshold
  k = 0.7
  r =random.random()

  if r > 0.7:
    # choose less fit individual
    return (index1 if fitness1 < fitness2 else index2)
  else:
    # choose more fit individual
    return (index1 if fitness1 > fitness2 else index2)


def ga(population):
  
  prev = 0
  count = 0

  population = sorted(population, reverse=True, key=fitness)

  # for each generation, repeat
  for i in range(generations):

    # add fitness of current_gen for graph
    fitness_gen.append(fitness(population[0]))

    # creata new empty generation
    new_generation = []
    
    # elitism
    # copy some of best solutions as it is
    for j in range(elitism_size):
      new_generation.append(population[j])

    # for rest of chromosomes, allow crossover and mutation
    for j in range(int((population_size - elitism_size)/2)):

      # select parents through tournament selection
      index1 = selection(population)
      index2 = selection(population)

      # fetch chromosomes
      individual1 = population[index1].copy()
      individual2 = population[index2].copy()

      # crossover with given probability
      r = random.random()
      if r < crossover_probability:
        individual1, individual2 = crossover(individual1, individual2)
      
      # mutate the offsprings at each locus with given probabilty
      individual1 = mutate(individual1)
      individual2 = mutate(individual2)      

      # add the offsprings in new generations
      new_generation.append(individual1)
      new_generation.append(individual2)
    
    # sort the new population and 
    # make it current generation
    new_generation = sorted(new_generation, reverse = True, key = fitness)
    population = new_generation.copy()

    if fitness(new_generation[0]) == prev:
      count += 1
    else:
      count = 0
      prev = fitness(new_generation[0])

    if count == 50:
      break

  return (population)


if __name__ == "__main__":

  with open("input/data.json", "r") as file:
    db = json.load(file)

  # data variables
  n = db["n"]
  m = db["m"]
  t = db["t"]
  ns = db["ns"]
  profit = db["profit"]
  time = db["time"]
  task_skills = db["task__skills"]
  team_skills = db["team__skills"]

  # GA parameter variables
  population_size = db["population_size"]
  elitism_size = db["elitism_size"]
  generations = db["generations"]
  crossover_probability = db["crossover_probability"]
  mutation_probability = db["mutation_probability"]

  # Fitness of each generation to be stored
  fitness_gen = []

  # generate initial population
  population = [create_individual() for _ in range(population_size)]

  # build a boolean matrix which tells whether a team member
  # can perform a particular task or not
  # based on its skills and skills required by a task
  canPerformTask = [
    [
      checkIfEligible(i, j) for j in range(n)
    ] for i in range(m)
  ]

  final_population = ga(population)

  print("Solution: ")
  print("Fitness = ", fitness(final_population[0]))
  print("chromosome = ", final_population[0])

  # plot the generation vs fitness graph
  plt.xlabel("generation")
  plt.ylabel("Fitness")
  plt.title("Fitness of solution = %s" % fitness(final_population[0]))
  plt.plot([i+1 for i in range(len(fitness_gen))], fitness_gen, 'b-')
  plt.show()