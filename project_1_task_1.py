# encoding: utf-8

from BinaryString import BinaryString
from InputMethods import readIntMin, readIntInterval, readFloatInterval, readIntInterval, readOption, readFloat
from NatureInspiredAlgorithms import geneticAlgorithm, hillClimbing, iterativeHillClimbing, simulatedAnnealing
import matplotlib.pyplot as plt
from random import random, randint
from copy import deepcopy

#DEFINIÇÃO DE CONSTANTES E VARIÁVEIS GLOBAIS
zero = BinaryString([1,1,1,1,0,1,1,0,1,1,1,1])
withElitism = False
shouldCrossover = False
crossoverProbability = 0
crossoverRangeStart = 0
crossoverRangeEnd = zero.size - 1
shouldMutate = False
mutationProbability = 0
#-------------------------------------------------------

#DEFINIÇÃO DE FUNÇÕES

#Calculo da aptidão da população
def fitnessCalculation(population):
	fitnessList = []
	bestFitness = 0
	bestIndex = 0
	for i in range(len(population)):
		fitnessList.append(zero.size - BinaryString.hammingDistance(zero,population[i]))
		if fitnessList[i] >= bestFitness:
			bestFitness = fitnessList[i]
			bestIndex = i
	return [fitnessList, bestIndex]

#Função que retorna o indicie da melhor aptidão de uma lista de fitness
def getBestFitnessIndex(fitnessList):
	bestFitness = 0
	bestIndex = 0
	for i in range(len(fitnessList)):		
		if fitnessList[i] >= bestFitness:
			bestFitness = fitnessList[i]
			bestIndex = i
	return bestIndex

#Seleção por roleta
def rouletteWheelSelection(population, fitnessList):
	if(len(population) != len(fitnessList)):
		raise Exception("Population and fitness list must be the same length")

	wheelSections = []
	selectedGenes = []
	newPopulation = []
	totalFitness = sum(fitnessList)

	for i in range(len(fitnessList)):
		#Definição das seções da roda 
		wheelSections.append(360*fitnessList[i] / float(totalFitness))
		#Sorteio do individuo para nova população
		selectedGenes.append(random() * 360)
		#Ajuste dos valores para obter valores entre 0 e 360
		if i > 0:
			wheelSections[i] = wheelSections[i-1] + wheelSections[i]
	
	#Substituicao dos individuos pelos sorteados
	for i in range(len(selectedGenes)):
		j = 0
		while j < len(wheelSections) and wheelSections[j] <= selectedGenes[i]:
			j+=1
		newPopulation.append(deepcopy(population[j]))

	#Caso o elitismo esteja habilitado, preserva o melhor gene na primeira posição
	if withElitism:
		bestIndex = getBestFitnessIndex(fitnessList)
		newPopulation[0]  = population[bestIndex]

	return newPopulation

#Crossover dois a dois
def crossover2by2(population, fitnessList):
	#Retorna a população sem alteração caso não deva fazer o crossover
	if not shouldCrossover:
		return population

	newPopulation = population
	#Para cada 2 individuos da população faça
	for i in range(0, len(population), 2):
		#Verifica se deve aplicar crossover para o par
		should = random() <= crossoverProbability
		if should:
			#Se sim, gera um ponto e cruza os indivíduos
			point = randint(crossoverRangeStart, crossoverRangeEnd)
			[newPopulation[i], newPopulation[i+1]] = BinaryString.crossover(population[i],population[i+1],point)
	return newPopulation

#Mutação simple um a um
def mutate(population):
	#Retorna a população sem alteração caso não deva ocorrer mutação
	if not shouldMutate:
		return population

	#Se o elitismo estiver habilitado não aplica a mutação para o melhor indivíduo
	if withElitism:
		[fitnessList, bestIndex] = fitnessCalculation(population)
		#Para cada individuo da população faça
		for i in range(len(population)):
			if i != bestIndex:
				#Aplica a função de mutação com a probabilidade dada
				population[i].mutate(mutationProbability)
	else:		
		#Para cada individuo da população faça
		for i in range(len(population)):
			#Aplica a função de mutação com a probabilidade dada
			population[i].mutate(mutationProbability)	

	return population

#Verificação de objetivo atingido
def equalsZero(fitnessList, bestIndex):
	if (fitnessList[bestIndex] == 12):
		return True
	return False

#Perturba x somando um valor aleatório
def disturbPlusRandom(x):
	newSize = randint(1, x.size)
	aux = BinaryString.newRandom(newSize)
	return BinaryString.binaryAdd(x, aux, False)

#Compara a fitness da string binaria com o esperado
def binaryEqualsZero(fitness):
	if fitness == 12:
		return True
	return False

#Avalia aptidão de x
def availX(x):
	return zero.size - BinaryString.hammingDistance(zero,x)

#Verifica se deve trocar pela nova aptidao
def shouldGetNewX(best, newFitness):
	if newFitness > best:
		return True
	return False

#Mudanca de temperatura
def decreasetemperature(t, it):
	return t * 0.8

#-------------------------------------------------------

#INICIO DA EXECUÇÃO
print("\nReconhecimento de padroes com algoritmo genetico")
print("------------------------------------------------")
print("Aproximar ao maximo a figura 0, representado por [1 1 1 1 0 1 1 0 1 1 1 1].")


algorithm = readIntInterval("\nDeseja utilizar que algoritmo?\n1 - Genetico\n2 - Subida de Colina\n3 - Subida de Colina Iterativa\n4 - Recozimento Simulado\n", 1, 4)
if algorithm == 1:
	popSize = 1
	while popSize % 2 == 1:
		popSize = readIntMin('Tamanho da populacao: ', 1)
		if popSize % 2 == 1:
			print('Populacao deve ser de tamanho par para aplicar o crossover 2 por 2!')

	withElitism = readOption('Deseja que a selecao permita o elitismo? (s/n)\n','s','n')

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
		mutationProbability = readFloatInterval("Probabilidade de mutacao dos individuos: ", 0, 1)
	else:
		mutationProbability = 0
			
	maxIt = readIntMin('Numero maximo de iteracoes do algoritmo: ',1)


	population = []
	for i in range(popSize):
		population.append(BinaryString.newRandom(zero.size))

	print('\nExecutando...')

	[population, fitnessList, bestGeneIndex, generationCount, avgFitness, bestFitness] = geneticAlgorithm(population, maxIt, rouletteWheelSelection, crossover2by2, mutate, fitnessCalculation, equalsZero)

	print('Finalizado!\n')
	print('Geracoes executadas: '+str(generationCount))

	printResults = readOption('\nDeseja ver a ultima geracao do algoritmo? (s/n)\n','s','n')

	if printResults:
		print('\nPopulacao final: ')
		for i in range(len(population)):
			print('['+population[i].toString() + '] - Fitness: '+ str(fitnessList[i]))
		print('Melhor gene:\n[' + population[bestGeneIndex].toString() +'] - Fitness:'+ str(fitnessList[bestGeneIndex]))

	plotGraphs = readOption('\nDeseja ver o grafico com a media de desempenho e o melhor desempenho de cada geracao? (s/n)\n','s','n')

	if plotGraphs:
		x = range(len(avgFitness))
		plt.plot(x,avgFitness, label="Average fitness")
		plt.plot(x,bestFitness, label="Best fitness")
		plt.legend()
		plt.show()
elif algorithm == 2:
	maxIt = readIntMin('Numero maximo de iteracoes do algoritmo: ',1)
	maxNoImprove = readIntMin('Numero maximo de iteracoes sem melhora do algoritmo: ',1)
	
	x = BinaryString.newRandom(zero.size)
		
	print('\nExecutando...')
	
	[x, bestFitness, achieved, fitness, generationCount] = hillClimbing(x, maxIt, maxNoImprove, disturbPlusRandom, availX, shouldGetNewX, binaryEqualsZero)

	print('Finalizado!\n')

	if achieved:
		print('Objetivo atingido!')
	else:
		print('Objetivo nao foi atingido!')

	print('Geracoes executadas: '+str(generationCount))

	printResults = readOption('\nDeseja ver o resultado encontrado? (s/n)\n','s','n')

	if printResults:
		print('Resultado encontrado:\n[' + x.toString() +'] - Fitness:'+ str(bestFitness))

	plotGraphs = readOption('\nDeseja ver o grafico com o desempenho cada iteracao? (s/n)\n','s','n')

	if plotGraphs:
		x = range(len(fitness))
		plt.plot(x,fitness, label="Desempenho")
		plt.legend()
		plt.show()
elif algorithm == 3:
	maxHillClimbIt = readIntMin('Numero maximo de execucoes do algoritmo de subida de colina: ',1)
	maxIt = readIntMin('Numero maximo de iteracoes do algoritmo de subida de colina: ',1)
	maxNoImprove = readIntMin('Numero maximo de iteracoes sem melhora do algoritmo de subida de colina: ',1)
	
	x = BinaryString.newRandom(zero.size)

	print('\nExecutando...')
	
	[x, bestFitness, achieved, fitness, generationCount] = iterativeHillClimbing(x, maxHillClimbIt, maxIt, maxNoImprove, disturbPlusRandom, availX, shouldGetNewX, binaryEqualsZero)

	print('Finalizado!\n')

	if achieved:
		print('Objetivo atingido!')
	else:
		print('Objetivo nao foi atingido!')

	print('Geracoes executadas: '+str(generationCount))

	printResults = readOption('\nDeseja ver o resultado encontrado? (s/n)\n','s','n')

	if printResults:
		print('Resultado encontrado:\n[' + x.toString() +'] - Fitness:'+ str(bestFitness))
	
	plotGraphs = readOption('\nDeseja ver o grafico com o desempenho a cada iteracao ? (s/n)\n','s','n')

	if plotGraphs:
		x = range(len(fitness))
		plt.plot(x,fitness, label="Desempenho")
		plt.legend()
		plt.show()			
elif algorithm == 4:
	maxIt = readIntMin('Numero maximo de iteracoes do algoritmo: ',1)
	maxNoImprove = readIntMin('Numero maximo de iteracoes sem melhora do algoritmo: ',1)
	initialTemperature = readFloat('Temperatura inicial do sistema: ')

	x = BinaryString.newRandom(zero.size)
		
	print('\nExecutando...')
	[x, bestFitness, achieved, fitness, generationCount] = simulatedAnnealing(x, maxIt, maxNoImprove, initialTemperature, disturbPlusRandom, availX, shouldGetNewX, decreasetemperature, binaryEqualsZero)

	print('Finalizado!\n')

	if achieved:
		print('Objetivo atingido!')
	else:
		print('Objetivo nao foi atingido!')

	print('Geracoes executadas: '+str(generationCount))

	printResults = readOption('\nDeseja ver o resultado encontrado? (s/n)\n','s','n')

	if printResults:
		print('Resultado encontrado:\n[' + x.toString() +'] - Fitness:'+ str(bestFitness))

	plotGraphs = readOption('\nDeseja ver o grafico com o desempenho cada iteracao? (s/n)\n','s','n')

	if plotGraphs:
		x = range(len(fitness))
		plt.plot(x,fitness, label="Desempenho")
		plt.legend()
		plt.show()

print('\nFinalizando script...')
