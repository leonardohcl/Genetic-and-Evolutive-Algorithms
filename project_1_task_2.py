# encoding: utf-8

from BinaryString import BinaryString
from InputMethods import readInt, readIntMin, readIntInterval, readFloatInterval, readIntInterval, readOption, readFloat
from NatureInspiredAlgorithms import geneticAlgorithm, hillClimbing, iterativeHillClimbing, simulatedAnnealing
import matplotlib.pyplot as plt
import time
import math
from random import random, randint
from copy import deepcopy

#DEFINIÇÃO DE CONSTANTES E VARIÁVEIS GLOBAIS
withElitism = False
shouldCrossover = False
crossoverProbability = 0
crossoverRangeStart = 0
crossoverRangeEnd = 0
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
		fitnessList.append(g(population[i].binToInt()))
		if fitnessList[i] > bestFitness:
			bestFitness = fitnessList[i]
			bestIndex = i
	return [fitnessList, bestIndex]

#g(x)
def g(x):
	x = float(x)
	y = (2**(-2*(((x-0.1)/0.9))**2))*((math.sin(5*math.pi*x))**6)
	return y

#Função que retorna o indicie da melhor aptidão de uma lista de fitness
def getBestFitnessIndex(fitnessList):
	bestFitness = 0
	bestIndex = 0
	for i in range(len(fitnessList)):		
		if fitnessList[i] > bestFitness:
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
def isMaxed(fitnessList, bestIndex):
	return False

#Perturba x somando um valor aleatório
def disturbPlusRandom(x):
	newSize = randint(1, x.size)
	aux = BinaryString.newRandom(newSize)
	return BinaryString.binaryAdd(x, aux, False)

#Compara a fitness da string binaria com o esperado
def binaryIsMaxed(fitness):
	return False

#Avalia aptidão de x
def availX(x):
	return g(x.binToInt())

#Verifica se deve trocar pela nova aptidao
def shouldGetNewX(best, newFitness):
	if newFitness > best:
		return True
	return False

#Mudanca de temperatura
def decreaseTemperature(t, it):
	return t * 0.8

#-------------------------------------------------------

#INICIO DA EXECUÇÃO
print("\nMinimizar funcao com algoritmo genetico")
print("------------------------------------------------")
print("Maximizar a funcao g(x) = (2^(-2((𝑥-0.1)/0.9))^2)(sin(5𝜋𝑥))^6")


algorithm = readIntInterval("\nDeseja utilizar que algoritmo?\n1 - Genetico\n2 - Subida de Colina\n3 - Subida de Colina Iterativa\n4 - Recozimento Simulado\n", 1, 4)
if algorithm == 1:
	print("\n------------------------------------------------")
	print('Algoritmo genetico:\n')

	intervalStart = readInt('Inicio do intervalo a encontrar o maximo: ')
	intervalEnd = readInt('Fim do intervalo a encontrar o maximo: ')

	minVal = BinaryString.newFromInt(intervalStart)
	maxVal = BinaryString.newFromInt(intervalEnd)

	if(maxVal.size > minVal.size):
		stringSize = maxVal.size
	else:
		stringSize = minVal.size

	popSize = 1
	while popSize % 2 == 1:
		popSize = readIntMin('Tamanho da populacao: ', 1)
		if popSize % 2 == 1:
			print('Populacao deve ser de tamanho par para aplicar o crossover 2 por 2!')

	withElitism = readOption('\nDeseja que a selecao permita o elitismo? (s/n)\n','s','n')

	shouldCrossover = readOption('\nDeseja que ocorra crossover dos individuos? (s/n)\n','s','n')		
	
	if shouldCrossover:
		crossoverProbability = readFloatInterval('Probabilidade de ocorrer o crossover: ', 0, 1)

		crossoverRangeStart = readIntInterval('Inicio do intervalo de indices que podem ser selecionados para o crossover: ', 0, stringSize - 1)
		
		crossoverRangeEnd = readIntInterval('Fim do intervalo de indices que podem ser selecionados para o crossover: ', crossoverRangeStart, stringSize - 1)
	else:
		crossoverRangeStart = 0
		crossoverRangeEnd = stringSize - 1
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
		didtnMakeIt = 0
		print('\nExecutando...')
		start = time.time()
		for i in range(n):	
			population = []
			for i in range(popSize):
				population.append(BinaryString.newRandom(stringSize))

			[population, fitnessList, bestGeneIndex, generationCount, avgFitness, bestFitness] = geneticAlgorithm(population, maxIt, rouletteWheelSelection, crossover2by2, mutate, fitnessCalculation, isMaxed)
			if fitnessList[bestGeneIndex] != 12:
				didtnMakeIt += 1
			itCountList.append(generationCount)
		end = time.time()
		elapsed = (end - start)*1000
		print('Finalizado em '+str(elapsed)+'ms\n')
		avgItCount = float(sum(itCountList))/len(itCountList)
		print('Nao convergiu antes do limite de execucoes '+str(didtnMakeIt)+' vezes')
		print('Media de iteracoes para cada execucao: '+str(avgItCount))
		
		plotGraphs = readOption('\nDeseja ver o grafico da quantidade de iteracoes para cada execucao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(itCountList))
			plt.plot(x,itCountList, label="Numero de execucoes")
			plt.legend()
			plt.show()
	else:
		population = []
		for i in range(popSize):
			population.append(BinaryString.newRandom(stringSize))

		print('\nExecutando...')
		start = time.time()
		[population, fitnessList, bestGeneIndex, generationCount, avgFitness, bestFitness] = geneticAlgorithm(population, maxIt, rouletteWheelSelection, crossover2by2, mutate, fitnessCalculation, isMaxed)
		end = time.time()
		elapsed = (end - start)*1000
		print('Finalizado em '+str(elapsed)+'ms\n')
		print('Geracoes executadas: '+str(generationCount))

		printResults = readOption('\nDeseja ver a ultima geracao do algoritmo? (s/n)\n','s','n')

		if printResults:
			print('\nPopulacao final: ')
			for i in range(len(population)):
				print('['+population[i].toString() + '] - Fitness: '+ str(fitnessList[i]))
			print('Melhor gene:\n[' + population[bestGeneIndex].toString() +'] = '+ str(population[bestGeneIndex].binToInt())+' - Fitness:'+ str(fitnessList[bestGeneIndex]))

		plotGraphs = readOption('\nDeseja ver o grafico com a media de desempenho e o melhor desempenho de cada geracao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(avgFitness))
			plt.plot(x,avgFitness, label="Average fitness")
			plt.plot(x,bestFitness, label="Best fitness")
			plt.legend()
			plt.show()
elif algorithm == 2:
	print("\n------------------------------------------------")
	print('Subida de colina:\n')
	
	intervalStart = readInt('Inicio do intervalo a encontrar o maximo: ')
	intervalEnd = readInt('Fim do intervalo a encontrar o maximo: ')

	minVal = BinaryString.newFromInt(intervalStart)
	maxVal = BinaryString.newFromInt(intervalEnd)

	if(maxVal.size > minVal.size):
		stringSize = maxVal.size
	else:
		stringSize = minVal.size

	maxIt = readIntMin('\nNumero maximo de iteracoes do algoritmo: ',1)
	maxNoImprove = readIntMin('Numero maximo de iteracoes sem melhora do algoritmo: ',1)
	
	multipleExecutions = readOption('\nDeseja executar diversas vezes com esse parametros para obter estatisticas? (s/n)\n','s','n')

	if multipleExecutions:
		n = readIntMin('Numero de execucoes do algoritmo: ', 1)
		itCountList = []
		didtnMakeIt = 0
		print('\nExecutando...')
		start = time.time()			
		for i in range(n):
			x = BinaryString.newRandom(stringSize)			
			
			[x, bestFitness, achieved, fitness, generationCount] = hillClimbing(x, maxIt, maxNoImprove, disturbPlusRandom, availX, shouldGetNewX, binaryIsMaxed)

			itCountList.append(generationCount)

			if not achieved:
				didtnMakeIt += 1

		end = time.time()
		elapsed = (end - start)*1000
		print('Finalizado em '+str(elapsed)+'ms\n')
		avgItCount = float(sum(itCountList))/len(itCountList)
		
		print('Nao convergiu antes do limite de execucoes '+str(didtnMakeIt)+' vezes')
		print('Media de iteracoes para cada execucao: '+str(avgItCount))
		plotGraphs = readOption('\nDeseja ver o grafico da quantidade de iteracoes para cada execucao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(itCountList))
			plt.plot(x,itCountList, label="Numero de execucoes")
			plt.legend()
			plt.show()

	else:
		x = BinaryString.newRandom(stringSize)
			
		print('\nExecutando...')
		start = time.time()
		
		[x, bestFitness, achieved, fitness, generationCount] = hillClimbing(x, maxIt, maxNoImprove, disturbPlusRandom, availX, shouldGetNewX, binaryIsMaxed)

		end = time.time()
		elapsed = (end - start)*1000
		print('Finalizado em '+str(elapsed)+'ms\n')

		if achieved:
			print('Objetivo atingido!')
		else:
			print('Objetivo nao foi atingido!')

		print('Geracoes executadas: '+str(generationCount))

		printResults = readOption('\nDeseja ver o resultado encontrado? (s/n)\n','s','n')

		if printResults:
			print('Resultado encontrado:\n[' + x.toString() +'] = '+ str(x.binToInt())+'  - Fitness:'+ str(bestFitness))

		plotGraphs = readOption('\nDeseja ver o grafico com o desempenho cada iteracao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(fitness))
			plt.plot(x,fitness, label="Desempenho")
			plt.legend()
			plt.show()
elif algorithm == 3:
	print("\n------------------------------------------------")
	print('Subida de colina iterativa:\n')
	intervalStart = readInt('Inicio do intervalo a encontrar o maximo: ')
	intervalEnd = readInt('Fim do intervalo a encontrar o maximo: ')

	minVal = BinaryString.newFromInt(intervalStart)
	maxVal = BinaryString.newFromInt(intervalEnd)

	if(maxVal.size > minVal.size):
		stringSize = maxVal.size
	else:
		stringSize = minVal.size
	maxHillClimbIt = readIntMin('\nNumero maximo de execucoes do algoritmo de subida de colina: ',1)
	maxIt = readIntMin('\nNumero maximo de iteracoes do algoritmo de subida de colina: ',1)
	maxNoImprove = readIntMin('Numero maximo de iteracoes sem melhora do algoritmo de subida de colina: ',1)
	
	multipleExecutions = readOption('\nDeseja executar diversas vezes com esse parametros para obter estatisticas? (s/n)\n','s','n')

	if multipleExecutions:
		n = readIntMin('Numero de execucoes do algoritmo: ', 1)
		itCountList = []
		didtnMakeIt = 0
		print('\nExecutando...')
		start = time.time()
		for i in range(n):
			x = BinaryString.newRandom(stringSize)
			[x, bestFitness, achieved, fitness, generationCount] = iterativeHillClimbing(x, maxHillClimbIt, maxIt, maxNoImprove, disturbPlusRandom, availX, shouldGetNewX, binaryIsMaxed)

			itCountList.append(generationCount)
			if not achieved:
				didtnMakeIt += 1

		end = time.time()
		elapsed = (end - start)*1000
		print('Finalizado em '+str(elapsed)+'ms\n')
		avgItCount = float(sum(itCountList))/len(itCountList)
		
		print('Nao convergiu antes do limite de execucoes '+str(didtnMakeIt)+' vezes')
		print('Media de iteracoes para cada execucao: '+str(avgItCount))
		plotGraphs = readOption('\nDeseja ver o grafico da quantidade de iteracoes para cada execucao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(itCountList))
			plt.plot(x,itCountList, label="Numero de execucoes")
			plt.legend()
			plt.show()
			
	else:
		x = BinaryString.newRandom(stringSize)

		print('\nExecutando...')
		start = time.time()
		[x, bestFitness, achieved, fitness, generationCount] = iterativeHillClimbing(x, maxHillClimbIt, maxIt, maxNoImprove, disturbPlusRandom, availX, shouldGetNewX, binaryIsMaxed)

		end = time.time()
		elapsed = (end - start)*1000
		print('Finalizado em '+str(elapsed)+'ms\n')

		if achieved:
			print('Objetivo atingido!')
		else:
			print('Objetivo nao foi atingido!')

		print('Geracoes executadas: '+str(generationCount))

		printResults = readOption('\nDeseja ver o resultado encontrado? (s/n)\n','s','n')

		if printResults:
			print('Resultado encontrado:\n[' + x.toString() +'] = '+ str(x.binToInt())+'  - Fitness:'+ str(bestFitness))
		
		plotGraphs = readOption('\nDeseja ver o grafico com o desempenho a cada iteracao ? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(fitness))
			plt.plot(x,fitness, label="Desempenho")
			plt.legend()
			plt.show()			
elif algorithm == 4:
	print("\n------------------------------------------------")
	print('Recozimento simulado:\n')

	intervalStart = readInt('Inicio do intervalo a encontrar o maximo: ')
	intervalEnd = readInt('Fim do intervalo a encontrar o maximo: ')

	minVal = BinaryString.newFromInt(intervalStart)
	maxVal = BinaryString.newFromInt(intervalEnd)

	if(maxVal.size > minVal.size):
		stringSize = maxVal.size
	else:
		stringSize = minVal.size


	maxIt = readIntMin('Numero maximo de iteracoes do algoritmo: ',1)
	maxNoImprove = readIntMin('Numero maximo de iteracoes sem melhora do algoritmo: ',1)
	initialTemperature = readFloat('Temperatura inicial do sistema: ')

	multipleExecutions = readOption('\nDeseja executar diversas vezes com esse parametros para obter estatisticas? (s/n)\n','s','n')

	if multipleExecutions:
		n = readIntMin('Numero de execucoes do algoritmo: ', 1)
		itCountList = []
		didtnMakeIt = 0
		print('\nExecutando...')
		start = time.time()
		for i in range(n):
			x = BinaryString.newRandom(stringSize)
			[x, bestFitness, achieved, fitness, generationCount] = simulatedAnnealing(x, maxIt, maxNoImprove, initialTemperature, disturbPlusRandom, availX, shouldGetNewX, decreaseTemperature, binaryIsMaxed)
			itCountList.append(generationCount)
			if not achieved:
				didtnMakeIt += 1

		end = time.time()
		elapsed = (end - start)*1000
		print('Finalizado em '+str(elapsed)+'ms\n')
		avgItCount = float(sum(itCountList))/len(itCountList)
		
		print('Nao convergiu antes do limite de execucoes '+str(didtnMakeIt)+' vezes')
		print('Media de iteracoes para cada execucao: '+str(avgItCount))
		plotGraphs = readOption('\nDeseja ver o grafico da quantidade de iteracoes para cada execucao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(itCountList))
			plt.plot(x,itCountList, label="Numero de execucoes")
			plt.legend()
			plt.show()
	else:	
		x = BinaryString.newRandom(stringSize)
		print('\nExecutando...')
		[x, bestFitness, achieved, fitness, generationCount] = simulatedAnnealing(x, maxIt, maxNoImprove, initialTemperature, disturbPlusRandom, availX, shouldGetNewX, decreaseTemperature, binaryIsMaxed)

		print('Finalizado!\n')

		if achieved:
			print('Objetivo atingido!')
		else:
			print('Objetivo nao foi atingido!')

		print('Geracoes executadas: '+str(generationCount))

		printResults = readOption('\nDeseja ver o resultado encontrado? (s/n)\n','s','n')

		if printResults:
			print('Resultado encontrado:\n[' + x.toString() +'] = '+ str(x.binToInt())+' - Fitness:'+ str(bestFitness))

		plotGraphs = readOption('\nDeseja ver o grafico com o desempenho cada iteracao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(fitness))
			plt.plot(x,fitness, label="Desempenho")
			plt.legend()
			plt.show()

print('\nFinalizando script...')
