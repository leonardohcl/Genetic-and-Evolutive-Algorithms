# encoding: utf-8

from BinaryString import BinaryString
from InputMethods import readIntMin, readFloatInterval, readIntInterval, readOption
from GeneticAlgorithm import geneticAlgorithm, rouletteWheelSelection, Crossover, Mutation

zero = BinaryString([1,1,1,1,0,1,1,0,1,1,1,1])

def fitnessCalc(binStr):
	return len(zero.bin) - BinaryString.hammingDistance(zero, binStr)

def bestFitness(fitnessList):
	best = 12 - fitnessList[0]
	bestI = 0
	for i in range(len(fitnessList)):
		comp = 12 - fitnessList[i]
		if(comp > best):
			best = comp
			bestI = i
	return [best, bestI]


print("\nReconhecimento de padroes com algoritmo genetico")
print("------------------------------------------------")
print("Aproximar ao maximo a figura 0, representado por [1 1 1 1 0 1 1 0 1 1 1 1].")

popSize = 1
while popSize % 2 == 1:
	popSize = readIntMin('Tamanho da populacao: ', 0)
	if popSize % 2 == 1:
		print('Populacao deve ser de tamanho par para facilitar crossover!')


shouldCrossover = readOption('Deseja que ocorra crossover dos individuos? (s/n)\n','s','n')

if shouldCrossover:
	crossoverProbability = readFloatInterval('Qual a probabilidade de ocorrer o crossover?\n', 0, 1)

	crossoverRangeStart = readIntInterval('Qual o inicio do intervalo de indices que podem ser selecionados para o crossover?\n', 0, zero.size - 1)
	
	crossoverRangeEnd = readIntInterval('Qual o fim do intervalo de indices que podem ser selecionados para o crossover?\n', crossoverRangeStart, zero.size - 1)
else:
	crossoverRangeStart = 0
	crossoverRangeEnd = zero.size - 1
	crossoverProbability = 0

shouldMutate = readOption('Deseja que ocorram mutacoes nos individuos? (s/n)\n','s','n')

if shouldMutate:
	mutationProp = readFloatInterval("Probabilidade de mutacao dos individuos: ", 0, 1)
else:
	mutationProp = 0
		
crossover = Crossover(shouldCrossover,crossoverProbability,crossoverRangeStart,crossoverRangeEnd,rouletteWheelSelection)
mutation = Mutation(shouldMutate, mutationProp)

population = []
for i in range(popSize):
	population.append(BinaryString.rand(zero.size))

geneticAlgorithm(population,150,crossover,mutation,12,fitnessCalc,bestFitness)