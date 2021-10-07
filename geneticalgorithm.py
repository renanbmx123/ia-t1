import time
from random import randint, random
from copy import deepcopy
from maze import MazeGame
from manhattan_dist import getManhattanDistance
from print_pretty import print_pretty


class GeneticAlgorithm:
    MOVE_LIMIT = 25
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

        self.createBasePopulation()
        self.GenerationalBest(t)

        for i in range(1, self.MAX_GENERATIONS):
            t = time.monotonic()
            self.generation += 1

            self.crossover()
            p = self.GenerationalBest(t)
            if p != None:
                self.solution = p
                break
        return self.solution[0]  # return best generation

    def GenerationalBest(self, startTime):
        best_solutions = []
        best = deepcopy(sorted(
            self.population, key=lambda chromosome: self.fitnessFunction(chromosome)
        )[:5])

        for i in range(len(best)):
            for j in range(self.MOVE_LIMIT):
                best[i][j] = self.GENES[best[i][j]]
        time_taken = time.monotonic() - startTime
        print(f'Generation {self.generation} - Time taken -  {(time_taken)}s')
        for item in best:
            score = self.fitnessFunction(item)
            print(f'{print_pretty(item)} , Score: {score}')
            if (score[0] == 0):
                best_solutions.append([item, score])
            else:
                # best_solutions.append([item, score])
                best_solutions = None

        return best_solutions

    def createBasePopulation(self):
        self.population = [
            [
                randint(self.GENES[0], self.GENES[-1]) for y in range(self.MOVE_LIMIT)
            ] for x in range(self.POPULATION_SIZE)
        ]

    def fitnessFunction(self, chromosome):
        game = MazeGame()
        game.open_maze("map.txt")

        # play the game
        for move in chromosome:
            if move == 0:
                game.up()
            elif move == 1:
                game.down()
            elif move == 2:
                game.left()
            elif move == 3:
                game.right()

        # distance
        distance = getManhattanDistance(game.x, game.y, game.goalX, game.goalY)

        # add penalty if there is a wall between current position and goal
        extra_penalty = game.blocked_goal()

        # minimize this score! tuple(score, moves)
        return (distance * extra_penalty + game.faults, game.steps)

    # crossover applies on a subset of the population that are fittest
    def crossover(self):
        newPopulation = []

        # sort population by fitness value then number of moves
        self.population.sort(key=lambda chromosome: self.fitnessFunction(chromosome))

        # consider 10% fittest population
        subset = self.population[:self.POPULATION_SIZE // 10]
        subsetSize = len(subset)

        for i in range(self.POPULATION_SIZE):
            firstParent = subset[randint(0, subsetSize - 1)]
            secondParent = subset[randint(0, subsetSize - 1)]

            # select a random crossover point in the genespace
            crossoverPoint = randint(0, self.MOVE_LIMIT - 1)

            newPopulation.append(
                self.mutate(firstParent[:crossoverPoint] + secondParent[crossoverPoint:])
            )

        self.population = newPopulation

    def mutate(self, chromosome):
        if random() < self.MUTATION_CHANCE:
            chromosome[randint(0, self.MOVE_LIMIT - 1)] = randint(self.GENES[0], self.GENES[-1])

        return chromosome
