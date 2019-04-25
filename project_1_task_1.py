# encoding: utf-8

from BinaryString import BinaryString
from InputMethods import readIntMin, readIntInterval, readFloatInterval, readIntInterval, readOption, readFloat, secondsToString
from NatureInspiredAlgorithms import geneticAlgorithm
import matplotlib.pyplot as plt
import time
import math
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

#Retorna a melhor aptidão de uma comparação
def newFitnessIsBetter(fitness, newFitness):
	if newFitness > fitness:
		return True
	return False
#-------------------------------------------------------

#INICIO DA EXECUÇÃO
print("\nReconhecimento de padroes com algoritmo genetico")
print("------------------------------------------------")
print("Aproximar ao maximo a figura 0, representado por [111101101111].")

popSize = 1
while popSize % 2 == 1:
	popSize = readIntMin('Tamanho da populacao: ', 1)
	if popSize % 2 == 1:
		print('Populacao deve ser de tamanho par para aplicar o crossover 2 por 2!')

withElitism = readOption('\nDeseja que a selecao permita o elitismo? (s/n)\n','s','n')

shouldCrossover = readOption('\nDeseja que ocorra crossover dos individuos? (s/n)\n','s','n')		

if shouldCrossover:
	crossoverProbability = readFloatInterval('Probabilidade de ocorrer o crossover: ', 0, 1)

	crossoverRangeStart = readIntInterval('Inicio do intervalo de indices que podem ser selecionados para o crossover: ', 0, zero.size - 1)
	
	crossoverRangeEnd = readIntInterval('Fim do intervalo de indices que podem ser selecionados para o crossover: ', crossoverRangeStart, zero.size - 1)
else:
	crossoverRangeStart = 0
	crossoverRangeEnd = zero.size - 1
	crossoverProbability = 0

shouldMutate = readOption('\nDeseja que ocorram mutacoes nos individuos? (s/n)\n','s','n')

if shouldMutate:
	mutationProbability = readFloatInterval("Probabilidade de mutacao dos individuos: ", 0, 1)
else:
	mutationProbability = 0
		
maxIt = readIntMin('\nNumero maximo de iteracoes do algoritmo: ', 1)

multipleExecutions = readOption('\nDeseja executar diversas vezes com esse parametros para obter estatisticas? (s/n)\n','s','n')

if multipleExecutions:
	n = readIntMin('Numero de execucoes do algoritmo: ', 1)
	itCountList = []
	itFitnnesList = []
	itAvgBestFitnessList = []
	didtnMakeIt = 0
	print('\nExecutando...')
	nextPoint = 0	
	start = time.time()
	for i in range(n):			
		population = []
		for j in range(popSize):
			population.append(BinaryString.newRandom(zero.size))

		[population, bestGene, bestFitness, lastFitnessList, lastBestGeneIndex, generationCount, avgFitnessList, bestFitnessList] = geneticAlgorithm(population, maxIt, rouletteWheelSelection, crossover2by2, mutate, fitnessCalculation, equalsZero, newFitnessIsBetter)

		if bestFitness != 12:
			didtnMakeIt += 1				
		
		itAvgBestFitnessList.append(sum(bestFitnessList)/len(bestFitnessList))
		itFitnnesList.append(bestFitness)
		itCountList.append(generationCount)

		prct = float(i)/n
		if(prct >= nextPoint):
			pointTime = time.time()						
			print('['+secondsToString(pointTime - start)+'] - '+str(100*prct)+'%')
			nextPoint += 0.1

	end = time.time()
	elapsed = end - start
	print('['+secondsToString(elapsed)+'] - Finalizado\n')

	avgItCount = float(sum(itCountList))/len(itCountList)
	avgItFitness = sum(itFitnnesList)/len(itFitnnesList)

	devItFitness = 0
	devItCount = 0
	for i in range(len(itFitnnesList)):
		devItFitness += (itFitnnesList[i] - avgItFitness)**2
		devItCount += (itCountList[i] - avgItCount)**2
	
	devItFitness = math.sqrt(devItFitness/len(itFitnnesList))
	devItCount = math.sqrt(devItCount/len(itCountList))


	print('\nMedia de iteracoes para cada execucao: '+str(avgItCount))
	print('Desvio padrao de iteracoes para cada execucao: '+str(devItCount))
	print('\nMedia de aptidao para cada execucao: '+str(avgItFitness))
	print('Desvio padrao de aptidao para cada execucao: '+str(devItFitness))

	print('\nExecucoes que pararam por atingir o maximo de iteracoes: '+str(didtnMakeIt) + ' de '+str(n))

	
	plotGraphs = readOption('\nDeseja ver o grafico da quantidade de iteracoes para cada execucao? (s/n)\n','s','n')

	if plotGraphs:
		x = range(len(itCountList))
		mean = len(x) * [avgItCount]
		plt.bar(x,itCountList)
		plt.plot(x,mean, 'r-', label="Mean")
		plt.ylabel('Iterations')
		plt.xlabel('Execution')
		plt.legend()
		plt.show()

	plotGraphs = readOption('\nDeseja ver o grafico do fitness para cada execucao? (s/n)\n','s','n')

	if plotGraphs:
		x = range(len(itFitnnesList))
		meanArray = len(x) * [avgItFitness]
		plt.plot(x,itFitnnesList, label="Best fitness this iteration")
		plt.plot(x,itAvgBestFitnessList, label="Average fitness this iteration")
		plt.ylabel('Fitness')
		plt.xlabel('Execution')
		plt.legend()
		plt.show()
else:
	population = []
	for i in range(popSize):
		population.append(BinaryString.newRandom(zero.size))

	print('\nExecutando...')
	start = time.time()
	[population, bestGene, bestFitness, lastFitnessList, lastBestGeneIndex, generationCount, avgFitnessList, bestFitnessList] = geneticAlgorithm(population, maxIt, rouletteWheelSelection, crossover2by2, mutate, fitnessCalculation, equalsZero, newFitnessIsBetter)
	end = time.time()
	elapsed = (end - start)*1000
	print('Finalizado em '+str(elapsed)+'ms\n')
	print('Geracoes executadas: '+str(generationCount))
	print('Melhor resultado encontrado: '+ bestGene.toString()+' - Fitness: '+ str(bestFitness))

	printResults = readOption('\nDeseja ver a ultima geracao do algoritmo? (s/n)\n','s','n')

	if printResults:
		print('\nPopulacao final: ')
		for i in range(len(population)):
			print('['+population[i].toString() + '] - Fitness: '+ str(lastFitnessList[i]))
		print('Melhor gene:\n[' + population[lastBestGeneIndex].toString() +'] - Fitness:'+ str(lastFitnessList[lastBestGeneIndex]))

	plotGraphs = readOption('\nDeseja ver o grafico com a media de desempenho e o melhor desempenho de cada geracao? (s/n)\n','s','n')

	if plotGraphs:
		x = range(len(avgFitnessList))
		plt.plot(x,avgFitnessList, label="Average fitness")
		plt.plot(x,bestFitnessList, label="Best fitness")
		plt.ylabel('Fitness')
		plt.xlabel('Generation')
		plt.legend()
		plt.show()

print('\nFinalizando script...')
