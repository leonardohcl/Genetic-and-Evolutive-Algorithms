# encoding: utf-8

from BinaryString import BinaryString
from InputMethods import readInt, readIntMin, readIntInterval, readFloatInterval, readIntInterval, readOption, readFloat
from NatureInspiredAlgorithms import geneticAlgorithm, hillClimbing, simulatedAnnealing
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

#f(x,y)
def f(x,y):
	x = float(x)
	y = float(y)
	z = ((1-x)**2) + 100*((y - (x**2))**2)
	return z

#Calculo da aptidão da população
def populationFitnessCalculation(population):	
	fitnessList = []
	bestFitness = float('inf')
	bestIndex = 0

	mid = population[0].size/2

	maxValueBS = BinaryString([0] + (mid-1)*[1])
	multiplier = 1.0/maxValueBS.binToInt()

	for i in range(len(population)):
		[x,y] = divideElement(population[i])
		xValue = abs(10 * x.binToInt() * multiplier) - 5
		yValue = abs(10 * y.binToInt() * multiplier) - 5
	 	value = f(xValue,yValue)
		fitnessList.append(value)
		if fitnessList[i] < bestFitness:
			bestFitness = fitnessList[i]
			bestIndex = i

	return [fitnessList, bestIndex]

#Calculo da aptidão e o valor de um individuo
def getElementValueAndFitness(el):
	mid = el.size/2

	maxValueBS = BinaryString([0] + (mid-1)*[1])
	multiplier = 1.0/maxValueBS.binToInt()

	[x,y] = divideElement(el)
	xValue = abs(10 * x.binToInt() * multiplier) - 5
	yValue = abs(10 * y.binToInt() * multiplier) - 5

	value = f(xValue,yValue)

	return [xValue, yValue, value]

#Calculo da aptidão de um individuo
def getElementFitness(x):	
	return getElementValueAndFitness(x)[2]
		
#Retorna o indicie do elemento com melhor aptidão
def getBestFitnessIndex(fitnessList):
	best = fitnessList[0]
	bestI = 0
	for i in range(len(fitnessList)):
		if fitnessList[i] < best:
			bestI = i
			best = fitnessList[i]
	
	return bestI

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
			[x1,y1] = divideElement(population[i])
			[x2,y2] = divideElement(population[i+1])

			point1 = randint(crossoverRangeStart, crossoverRangeEnd)
			point2 = randint(crossoverRangeStart, crossoverRangeEnd)

			[crossX1, crossX2] = BinaryString.crossover(x1,x2,point1)
			[crossY1, crossY2] = BinaryString.crossover(y1,y2,point2)

			newPopulation[i] = BinaryString(crossX1.bin + crossY1.bin)
			newPopulation[i+1] = BinaryString(crossX2.bin + crossY2.bin)
	return newPopulation

#Mutação simple um a um
def mutate(population):
	#Retorna a população sem alteração caso não deva ocorrer mutação
	if not shouldMutate:
		return population

	#Se o elitismo estiver habilitado não aplica a mutação para o melhor indivíduo
	if withElitism:
		[fitnessList, bestIndex] = populationFitnessCalculation(population)
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

#Verificação se o algoritmo genético pode parar a execução
def shouldStop(fitnessList, bestIndex):
	return False

#Retorna a melhor aptidão de uma comparação
def newFitnessIsBetter(fitness, newFitness):
	if newFitness < fitness:
		return True
	return False

#Retorna BinaryString de x e y dado um elemento BinaryString
def divideElement(el):
	mid = el.size/2
	xList = el.bin[:mid]
	yList = el.bin[mid:]
	x = BinaryString(xList)
	y = BinaryString(yList)
	return [x,y]


#-------------------------------------------------------

#INICIO DA EXECUÇÃO
print("\nMinimizar funcao com algoritmo genetico")
print("------------------------------------------------")
print("Minimzar a funcao f(x,y) = ((1-x)^2) + 100*((y - (x^2))^2)")

stringSize = readIntMin('Tamanho da bitstring que representa x e y: ', 2)

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

maxItNoImprove = readIntMin('\nNumero maximo de iteracoes do algoritmo sem evoluir a aptidao: ', 1)

multipleExecutions = readOption('\nDeseja executar diversas vezes com esse parametros para obter estatisticas? (s/n)\n','s','n')

#Dobra o tamanho para considerar dois valores em um individuo
stringSize = stringSize * 2

if multipleExecutions:
	n = readIntMin('Numero de execucoes do algoritmo: ', 1)
	itCountList = []
	itAvgBestFitnessList = []
	itFitnnesList = []
	bestGeneAmongIts = BinaryString([0,1,0,1])
	bestFitnessAmongIts = float('inf')
	print('\nExecutando...')
	start = time.time()
	for i in range(n):	
		population = []
		for i in range(popSize):
			population.append(BinaryString.newRandom(stringSize))

		[population, bestGene, bestFitness, lastFitnessList, lastBestGeneIndex, generationCount, avgFitnessList, bestFitnessList] = geneticAlgorithm(population, maxIt,rouletteWheelSelection, crossover2by2, mutate, populationFitnessCalculation, shouldStop, newFitnessIsBetter, maxItNoImprove)

		itCountList.append(generationCount)
		itFitnnesList.append(bestFitness)
		itAvgBestFitnessList.append(sum(bestFitnessList)/len(bestFitnessList))

		if newFitnessIsBetter(bestFitnessAmongIts, bestFitness):
			bestFitnessAmongIts = bestFitness
			bestGeneAmongIts = bestGene

	end = time.time()
	elapsed = (end - start)*1000
	print('Finalizado em '+str(elapsed)+'ms\n')					

	[bestXValue, bestYValue, bestValue] = getElementValueAndFitness(bestGene)
	print('Valor minimo atingido: f('+str(bestXValue)+','+str(bestYValue)+') = '+ str(bestFitness))
	
	avgItCount = float(sum(itCountList))/len(itCountList)
	print('Media de iteracoes para cada execucao: '+str(avgItCount))

	avgItFitness = sum(itFitnnesList)/len(itFitnnesList)
	print('Media de aptidao para cada execucao: '+str(avgItFitness))
	
	plotGraphs = readOption('\nDeseja ver o grafico da quantidade de iteracoes para cada execucao? (s/n)\n','s','n')

	if plotGraphs:
		x = range(len(itCountList))
		meanArray = len(x) * [avgItCount]
		plt.plot(x,itCountList)
		plt.plot(x,meanArray, label="Mean")
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
		population.append(BinaryString.newRandom(stringSize))
	
	print('\nExecutando...')
	start = time.time()

	[population, bestGene, bestFitness, lastFitnessList, lastBestGeneIndex, generationCount, avgFitnessList, bestFitnessList] = geneticAlgorithm(population, maxIt,rouletteWheelSelection, crossover2by2, mutate, populationFitnessCalculation, shouldStop, newFitnessIsBetter, maxItNoImprove)

	end = time.time()
	elapsed = (end - start)*1000

	[bestXValue, bestYValue, bestValue] = getElementValueAndFitness(bestGene)
	print('Finalizado em '+str(elapsed)+'ms\n')
	print('Geracoes executadas: '+str(generationCount))
	print('Valor minimo atingido: f('+str(bestXValue)+','+str(bestYValue)+') = '+ str(bestFitness))

	printResults = readOption('\nDeseja ver a ultima geracao do algoritmo? (s/n)\n','s','n')

	if printResults:
		print('\nPopulacao final: ')
		for i in range(len(population)):
			[binX,binY] = divideElement(population[i])
			print('['+binX.toString() + '],['+binY.toString()+'] - Fitness: '+ str(lastFitnessList[i]))

		[binX,binY] = divideElement(population[lastBestGeneIndex])
		[valX,valY,val] = getElementValueAndFitness(population[lastBestGeneIndex])
		print('Melhor gene:\n['+binX.toString() + '],['+binY.toString()+'] = '+ str(valX)+','+str(valY)+' - Fitness:'+ str(lastFitnessList[lastBestGeneIndex]))

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
