# encoding: utf-8

from BinaryString import BinaryString
from InputMethods import readIntMin, readFloatInterval, readIntInterval, readOption
from GeneticAlgorithm import geneticAlgorithm, Crossover, Mutation, crossover2by2
import matplotlib.pyplot as plt

zero = BinaryString([1,1,1,1,0,1,1,0,1,1,1,1])

def fitnessCalculation(binStr):
	return len(zero.bin) - BinaryString.hammingDistance(zero, binStr)

def getBestFitness(fitnessList):
	best = 12 - fitnessList[0]
	bestI = 0
	for i in range(len(fitnessList)):
		if(fitnessList[i] > best):
			best = fitnessList[i]
			bestI = i
	return [best, bestI]


def targetFitnessAchieved(bestFitness, population):
	if bestFitness == 12:
		return True
	return False

print("\nReconhecimento de padroes com algoritmo genetico")
print("------------------------------------------------")
print("Aproximar ao maximo a figura 0, representado por [1 1 1 1 0 1 1 0 1 1 1 1].")

popSize = 1
while popSize % 2 == 1:
	popSize = readIntMin('Tamanho da populacao: ', 1)
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
		
maxIt = readIntMin('Numero maximos de iteracoes do algoritmo: ',1)

crossover = Crossover(shouldCrossover,crossoverProbability,crossoverRangeStart,crossoverRangeEnd, crossover2by2)
mutation = Mutation(shouldMutate, mutationProp)

population = []
for i in range(popSize):
	population.append(BinaryString.rand(zero.size))

print('\nExecutando...')

[population, fitnessList, numGenerations, avgFitness, bestFitness, bestFitnessIndex] = geneticAlgorithm(population,maxIt,crossover,mutation,targetFitnessAchieved,fitnessCalculation,getBestFitness)

print('Finalizado!\n')
print('Geracoes executadas: '+str(numGenerations))

printResults = readOption('\nDeseja ver a ultima geracao do algoritmo? (s/n)\n','s','n')

if printResults:
	print('\nPopulacao final: ')
	for i in range(len(population)):
		print('['+population[i].toString() + '] - Fitness: '+ str(fitnessList[i]))
	print('Melhor gene:\n[' + population[bestFitnessIndex].toString() +'] - Fitness:'+ str(fitnessList[bestFitnessIndex]))

plotGraphs = readOption('\nDeseja ver o grafico com a media de desempenho e o melhor desempenho de cada geracao? (s/n)\n','s','n')

if plotGraphs:
	x = range(len(avgFitness))
	plt.plot(x,avgFitness, label="Fitness media")
	plt.plot(x,bestFitness, label="Melhor Fitness")
	plt.legend()
	plt.show()

print('\nFinalizando script...')