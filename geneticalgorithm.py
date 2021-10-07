import time
from random import randint, random
from copy import deepcopy
from maze import Maze
from manhattan_dist import getManhattanDistance
from print_pretty import print_pretty


class GeneticAlgorithm:
    MOVE_LIMIT = 50
    POPULATION_SIZE = 10000
    MUTATION_CHANCE = 0.9  # 90% chance at mutation
    GENES = [0, 1, 2, 3]  # up, down, left, right
    MAX_GENERATIONS = 1000000

    def __init__(self):
        self.population = []
        self.generation = 1
        self.solution = []

    def run(self):
        t = time.monotonic()

        self.create_base_population()
        self.best_generation(t)

        for i in range(1, self.MAX_GENERATIONS):
            t = time.monotonic()
            self.generation += 1

            self.crossover()
            p = self.best_generation(t)
            if p != None:
                self.solution = p
                break
        return p

    def best_generation(self, start_time):
        best_solutions = []
        best = deepcopy(sorted(
            self.population, key=lambda chromosome: self.fitness_function(chromosome)
        )[:5])

        for i in range(len(best)):
            for j in range(self.MOVE_LIMIT):
                best[i][j] = self.GENES[best[i][j]]
        time_taken = time.monotonic() - start_time
        print(f'Generation {self.generation} - Time taken -  {time_taken}s')
        for item in best:
            score = self.fitness_function(item)
            print(f'{print_pretty(item)} , Score: {score}')
            if score[0] == 0:
                best_solutions.append([item, score])
            else:
                # best_solutions.append([item, score])
                best_solutions = None

        return best_solutions

    def create_base_population(self):
        self.population = [
            [
                randint(self.GENES[0], self.GENES[-1]) for y in range(self.MOVE_LIMIT)
            ] for x in range(self.POPULATION_SIZE)
        ]

    def fitness_function(self, chromosome):
        maze = Maze()
        maze.open_maze("map.txt")
        # play the game
        for move in chromosome:
            if move == 0:
                maze.up()
            elif move == 1:
                maze.down()
            elif move == 2:
                maze.left()
            elif move == 3:
                maze.right()

        # distance
        distance = getManhattanDistance(maze.x, maze.y, maze.goalX, maze.goalY)

        # add penalty if there is a wall between current position and goal
        extra_penalty = maze.blocked_goal()

        # minimize this score! tuple(score, moves)
        return distance * extra_penalty + maze.faults, maze.steps

    # crossover applies on a subset of the population that are fittest
    def crossover(self):
        new_population = []

        # sort population by fitness value then number of moves
        self.population.sort(key=lambda chromosome: self.fitness_function(chromosome))

        # consider 10% fittest population
        subset = self.population[:self.POPULATION_SIZE // 10]
        subset_size = len(subset)

        for i in range(self.POPULATION_SIZE):
            first_parent = subset[randint(0, subset_size - 1)]
            second_parent = subset[randint(0, subset_size - 1)]

            # select a random crossover point in the genespace
            crossover_point = randint(0, self.MOVE_LIMIT - 1)

            new_population.append(
                self.mutate(first_parent[:crossover_point] + second_parent[crossover_point:])
            )

        self.population = new_population

    def mutate(self, chromosome):
        if random() < self.MUTATION_CHANCE:
            chromosome[randint(0, self.MOVE_LIMIT - 1)] = randint(self.GENES[0], self.GENES[-1])

        return chromosome
