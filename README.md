# T1 Artificial Intelligence
## Maze Generation
for maze generation we read a text file with maze configuration. Each character in text file
represents an object in maze.</br>

<ul>
<li>0 is a ground</li>
<li>1 is a wall</li>
<li>E represent initial position, located at <0,0> position</li>
<li>S represent the goal, located at <11,11> position</li>
</ul>
 
## Genetic algorithm implementation
The genetic algorithm implementation is made using python class named GA.
This class implements all necessaries functions for algorithm works.
### Base population
This function creates the base population, based on population size and all the genetic information.
`` def createBasePopulation(self):
        self.population = [
            [
                randint(self.GENES[0], self.GENES[-1]) for y in range(self.MOVE_LIMIT)
            ] for x in range(self.POPULATION_SIZE)
        ]``
## Fitness function
This function compute all moves in a population, and compute score.
To calculate distance betwen the actual position and goal, 
we use a Manhattan to calculate the distance.
## Mutate
The mutate function generate a mutation on the population, base te percentage value of a mutation can occur.
## Crossover
In crossover function we use
## GUI
wxWidgets is used for this project.  
## Usage
###Run
``pip install -r requirements.txt``
``python main.py``
