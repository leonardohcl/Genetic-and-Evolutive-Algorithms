# encoding: utf-8

from BinaryString import BinaryString
from InputMethods import readIntMin, readFloatInterval, readIntInterval, readOption
from NatureInspiredAlgorithms import geneticAlgorithm
import matplotlib.pyplot as plt
from random import random, randint
from copy import deepcopy

#DEFINIÇÃO DE CONSTANTES E VARIÁVEIS GLOBAIS
zero = BinaryString([1,1,1,1,0,1,1,0,1,1,1,1])
shouldCrossover = False
crossoverProbability = 0
crossoverRangeStart = 0
crossoverRangeEnd = zero.size - 1
shouldMutate = False
mutationProbability = 0

#DEFINIÇÃO DE FUNÇÕES

#Calculo da aptidão da população
def fitnessCalculation(population):
	fitnessList = []
	bestFitness = 0
	bestIndex = -1
	for i in range(len(population)):
		fitnessList.append(zero.size - BinaryString.hammingDistance(zero,population[i]))
		if fitnessList[i] >= bestFitness:
			bestFitness = fitnessList[i]
			bestIndex = i

	return [fitnessList, bestIndex]

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

#INICIO DO ALGORITMO
print("\nReconhecimento de padroes com algoritmo genetico")
print("------------------------------------------------")
print("Aproximar ao maximo a figura 0, representado por [1 1 1 1 0 1 1 0 1 1 1 1].")

popSize = 1
while popSize % 2 == 1:
	popSize = readIntMin('Tamanho da populacao: ', 1)
	if popSize % 2 == 1:
		print('Populacao deve ser de tamanho par para aplicar o crossover 2 por 2!')


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
		
maxIt = readIntMin('Numero maximos de iteracoes do algoritmo: ',1)


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

print('\nFinalizando script...')