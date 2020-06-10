import json
import random

# problem parameters
n_tasks = 1000
n_members = 25
n_skills = 15
time_limit = 150
max_time_task = 10

db = {
	"n": n_tasks,
	"m": n_members,
  "ns": n_skills,
	"t": time_limit,

  # ga paramaters
  "population_size": 50,
  "elitism_size": 4,
  "generations": 10000,
  "crossover_probability": 0.8,
  "mutation_probability": 0.05,

  # input matrices
	"profit": [random.randint(1, 10) for _ in range(n_tasks)],
	"time": [
            [random.randint(1, 2) for _ in range(n_tasks)] for _ in range(n_members)
          ],
  "task__skills": [
                    [random.choice([1, 0]) for _ in range(n_skills)] for _ in range(n_tasks)
                  ],
  "team__skills": [
                    [random.choice([1, 0]) for _ in range(n_skills)] for _ in range(n_members)
                  ]
}


with open("input/data.json", "w") as file:
    json.dump(db, file, indent=2)