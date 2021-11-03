import random

bestFitnessGeneration = []
averageFitnessGeneration = []
worstFitnessGeneration = []

populationSize = 4
totalQtyAssessments = 20
currentQtyAssessments = 0
percentageMutation = 3

population = []
nextPopulation = []
fitness = [0] * populationSize
fitnessNextPopulation = [0] * (populationSize + 1)
indexBetterSolution = 0
indexWorstSolution = 0

backpackSize = 190
punishment = 15
profitObjects = [50, 50, 64, 46, 50, 5]
weightObjects = [56, 59, 80, 64, 75, 17]
solutionSize = len(profitObjects)

result = []

def evaluateSolution(fitness, population, index):
	fitness[index] = objectiveFunction( population[index])


def evaluatePopulation(fitness, population, populationSize):
	for i in range(populationSize):
		evaluateSolution( fitness, population, i)


def identifyBestSolution(fitness, populationSize):
	indexBetterSolution = 0
	for i in range(populationSize):
		if fitness[indexBetterSolution] < fitness[i]:
			indexBetterSolution = i
	return indexBetterSolution


def elitism(populationSize, population, fitness, fitnessNextPopulation, nextPopulation):
	indexBetterSolution = identifyBestSolution(fitness, populationSize)
	nextPopulation[populationSize] = population[indexBetterSolution]
	fitnessNextPopulation[populationSize] = fitness[indexBetterSolution]

	return indexBetterSolution


def mutation(solutionSize, percentageMutation, population, nextPopulation, index):
	for i in range(solutionSize):
		if random.randint(0, 100) <= percentageMutation:
			if population[index][i] == 0:
				nextPopulation[index][i] = 1
			else:
				nextPopulation[index][i] = 0
		else:
			nextPopulation[index][i] = population[index][i]


def identifyWorstSolutionNextPopulation(populationSize, fitnessNextPopulation):
	indexWorstSolution = 0
	for i in range(populationSize+1):
		if fitnessNextPopulation[indexWorstSolution] > fitnessNextPopulation[i]:
			indexWorstSolution = i
	return indexWorstSolution


def identifyWorstSolutionCurrentPopulation(populationSize, fitness):
	indexWorstSolution = 0
	for i in range(populationSize):
		if fitness[indexWorstSolution] > fitness[i]:
			indexWorstSolution = i
	return indexWorstSolution


def generateNextPopulation(nextPopulation, fitnessNextPopulation, populationSize):
	worse = identifyWorstSolutionNextPopulation(populationSize, fitnessNextPopulation)
	del nextPopulation[worse]
	del fitnessNextPopulation[worse]

	population = nextPopulation
	fitness = fitnessNextPopulation

	nextPopulation.append(nextPopulation[0])
	fitnessNextPopulation.append(fitnessNextPopulation[0])

	return population, fitness


def stopCriterionReached(currentQtyAssessments, totalQtyAssessments):
	return currentQtyAssessments >= totalQtyAssessments


def reportConvergenceGeneration(fitness, bestFitnessGeneration, averageFitnessGeneration, worstFitnessGeneration, populationSize):
	bestFitnessGeneration.append(fitness[identifyBestSolution(fitness, populationSize)])
	worstFitnessGeneration.append(fitness[identifyWorstSolutionCurrentPopulation(populationSize, fitness)])
	average = 0

	for i in fitness:
		average = average+i

	averageFitnessGeneration.append(average/len(fitness))


def populationAlgorithm(population, fitness):

	for i in range(populationSize):
		population.append([0] * solutionSize)
		nextPopulation.append([0] * solutionSize)
	nextPopulation.append([0] * solutionSize)

	for i in range(populationSize):
		for j in range(solutionSize):
			population[i][j] = random.randint(0, 1)
	evaluatePopulation( fitness, population, populationSize)
	currentQtyAssessments = populationSize
	reportConvergenceGeneration(fitness, bestFitnessGeneration, averageFitnessGeneration, worstFitnessGeneration, populationSize)
	count = 0
	while not stopCriterionReached(currentQtyAssessments, totalQtyAssessments):
		indexBetterSolution = elitism(populationSize, population, fitness, fitnessNextPopulation, nextPopulation)
		for i in range(populationSize):
			mutation(solutionSize, percentageMutation, population, nextPopulation, i)
			fitnessNextPopulation[i] = objectiveFunction( nextPopulation[i])
			currentQtyAssessments = currentQtyAssessments + 1
		population, fitness = generateNextPopulation(nextPopulation, fitnessNextPopulation, populationSize)
		reportConvergenceGeneration(fitness, bestFitnessGeneration, averageFitnessGeneration, worstFitnessGeneration, populationSize)
		count = count + 1
	
	print("Melhor indivíduo")
	bestEnd = identifyBestSolution(fitness, populationSize)
	print(population[bestEnd])
	print("Fitness =", fitness[bestEnd])
	print("")

	return fitness[bestEnd], bestFitnessGeneration, averageFitnessGeneration, worstFitnessGeneration


def objectiveFunction(solution):
  fitness = 0
  weight = 0
  for i in range(len(solution)):
    fitness = fitness + (solution[i] * profitObjects[i])
    weight = weight + (solution[i] * weightObjects[i])
  
  if (weight > backpackSize):
    fitness = fitness - punishment

  return fitness

# RODANDO 30 VEZES O ALGORITMO
do = 30
while do >= 0:
  res = populationAlgorithm(population, fitness)
  do = do - 1