# encoding: utf-8

from BinaryString import BinaryString
from InputMethods import readInt, readIntMin, readIntInterval, readFloatInterval, readIntInterval, readOption, readFloat, secondsToString
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

#g(x)
def g(x):
	x = float(x)
	y = (2**(-2*(((x-0.1)/0.9))**2))*((math.sin(5*math.pi*x))**6)
	return y

#Calculo da aptidão da população
def populationFitnessCalculation(population):	
	fitnessList = []
	bestFitness = 0
	bestIndex = 0
	maxValueBS = BinaryString([0] + (population[0].size-1)*[1])
	multiplier = 1.0/maxValueBS.binToInt()	
	for i in range(len(population)):
		value = abs(population[i].binToInt() * multiplier)
		fitnessList.append(g(value))
		if fitnessList[i] > bestFitness:
			bestFitness = fitnessList[i]
			bestIndex = i

	return [fitnessList, bestIndex]

#Calculo da aptidão e o valor de um individuo
def getElementValueAndFitness(x):	
	maxValueBS = BinaryString([0] + (x.size-1)*[1])
	multiplier = 1.0/maxValueBS.binToInt()	
	value = abs(x.binToInt() * multiplier)
	return [value, g(value)]

#Calculo da aptidão de um individuo
def getElementFitness(x):	
	return getElementValueAndFitness(x)[1]
		
#Retorna o indicie do elemento com melhor aptidão
def getBestFitnessIndex(fitnessList):
	best = fitnessList[0]
	bestI = 0
	for i in range(len(fitnessList)):
		if fitnessList[i] > best:
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
def geneticAlgorithmShouldStop(fitnessList, bestIndex):
	return False
def hillClimbingShouldStop(bestFitness):
	return False
def simulatedAnnealingShouldStop(bestFitness):
	return False

#Retorna a melhor aptidão de uma comparação
def newFitnessIsBetter(fitness, newFitness):
	if newFitness > fitness:
		return True
	return False

#Mostra o ponto na curva
def plotPointOnCurve(point):
	x = []
	y = []
	for i in range(100):
		x.append(i * 0.01)
		y.append(g(x[i]))
	[px, py] = getElementValueAndFitness(point)
	plt.plot(x,y)
	plt.plot(px,py,'ro')
	plt.ylabel('g(x)')
	plt.xlabel('x')
	plt.show()

#Função que perturba x somando ou subtraindo em 1
def disturbPlusOne(x):
	xValue = x.binToInt()
	plusOne = BinaryString.newFromInt(xValue + 1)
	minusOne = BinaryString.newFromInt(xValue - 1)
	fitnessPlusOne = getElementFitness(plusOne)
	fitnessMinusOne = getElementFitness(minusOne)
		
	if fitnessMinusOne > fitnessPlusOne:
		return BinaryString.changeSize(minusOne, x.size)
	return BinaryString.changeSize(plusOne, x.size)

#Função que perturba x somando um valor aleatorio
def disturbMutating(x):
	newBinStr = BinaryString(x.bin)
	newBinStr.mutate(0.1)
	return newBinStr
	
#Funcao que decrementa a temperatura
def lowerTemperature(t, it):
	return t*0.8
#-------------------------------------------------------

#INICIO DA EXECUÇÃO
print("\Maximizar funcao com algoritmos inspirados na natureza")
print("------------------------------------------------")
print("Maximizar a funcao g(x) = (2^(-2((x-0.1)/0.9))^2)(sin(5pix))^6")


algorithm = readIntInterval("\nDeseja utilizar que algoritmo?\n1 - Genetico\n2 - Subida de Colina\n3 - Recozimento Simulado\n", 1, 3)
if algorithm == 1:
	print("\n------------------------------------------------")
	print('Algoritmo genetico:\n')

	stringSize = readIntMin('Tamanho da bitstring que representa x: ', 2)
	
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
	
	if multipleExecutions:
		n = readIntMin('Numero de execucoes do algoritmo: ', 1)
		itCountList = []
		itFitnnesList = []
		itSolutionList = []
		bestGeneAmongIts = BinaryString([0,0])
		bestFitnessAmongIts = 0
		gotToLimitIt = 0
		nextPoint = 0
		print('\nExecutando...')
		start = time.time()
		for i in range(n):	
		 	population = []
		 	for j in range(popSize):
		 		population.append(BinaryString.newRandom(stringSize))

			[population, bestGene, bestFitness, lastFitnessList, lastBestGeneIndex, generationCount, avgFitnessList, bestFitnessList] = geneticAlgorithm(population, maxIt,rouletteWheelSelection, crossover2by2, mutate, populationFitnessCalculation, geneticAlgorithmShouldStop, newFitnessIsBetter, maxItNoImprove)

		 	itCountList.append(generationCount)
			itFitnnesList.append(bestFitness)
			itSolutionList.append(bestGene)

			if generationCount >= maxIt:
				gotToLimitIt += 1

			if newFitnessIsBetter(bestFitnessAmongIts, bestFitness):
				bestFitnessAmongIts = bestFitness
				bestGeneAmongIts = bestGene

			prct = float(i)/n
			if(prct >= nextPoint):
				pointTime = time.time()						
				print('['+secondsToString(pointTime - start)+'] - '+str(100*prct)+'%')
				nextPoint += 0.1

		end = time.time()
		elapsed = end - start
		print('['+secondsToString(elapsed)+'] - Finalizado\n')					

		bestGeneValue = getElementValueAndFitness(bestGeneAmongIts)[0]
		print('Valor maximo atingido: g('+str(bestGeneValue)+')='+ str(bestFitnessAmongIts))
		
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

		print('\nExecucoes que pararam por atingir o maximo de iteracoes: '+str(gotToLimitIt) + ' de '+str(n))

		
		plotGraphs = readOption('\nDeseja ver o grafico da quantidade de iteracoes para cada execucao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(itCountList))
			mean = len(x) * [avgItCount]
			plt.bar(x,itCountList)
			plt.plot(x,mean,'r-',label="Mean")
			plt.ylabel('Iterations')
			plt.xlabel('Execution')
			plt.legend()
			plt.show()

		plotGraphs = readOption('\nDeseja ver o grafico do fitness para cada execucao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(itFitnnesList))
			mean = len(x) * [avgItFitness]
			plt.plot(x,itFitnnesList, label="Best fitness")
			plt.plot(x,mean,'r-', label="Mean")
			plt.ylabel('Best Fitness')
			plt.xlabel('Execution')
			plt.legend()
			plt.show()
		
		plotGraphs = readOption('\nDeseja ver os pontos maximos encontrados na curva? (s/n)\n','s','n')

		if plotGraphs:
			px = []
			py = []
			for i in range(len(itSolutionList)):
				[val, gx] = getElementValueAndFitness(itSolutionList[i])
				px.append(val) 
				py.append(gx)
			x = []
			y = []
			for i in range(100):
				x.append(i * 0.01)
				y.append(g(x[i])) 
			plt.plot(x,y)
			plt.plot(px,py,'ro',label="Max points found")
			plt.ylabel('g(x)')
			plt.xlabel('x')
			plt.legend()
			plt.show()
	else:
		population = []
		for i in range(popSize):
			population.append(BinaryString.newRandom(stringSize))
		
		print('\nExecutando...')
		start = time.time()

		[population, bestGene, bestFitness, lastFitnessList, lastBestGeneIndex, generationCount, avgFitnessList, bestFitnessList] = geneticAlgorithm(population, maxIt,rouletteWheelSelection, crossover2by2, mutate, populationFitnessCalculation, geneticAlgorithmShouldStop, newFitnessIsBetter, maxItNoImprove)

		end = time.time()
		elapsed = (end - start)*1000

		bestGeneValue = getElementValueAndFitness(bestGene)[0]
		print('Finalizado em '+str(elapsed)+'ms\n')
		print('Geracoes executadas: '+str(generationCount))
		print('Valor maximo atingido: g('+str(bestGeneValue)+')='+ str(bestFitness))

		printResults = readOption('\nDeseja ver a ultima geracao do algoritmo? (s/n)\n','s','n')

		if printResults:
			print('\nPopulacao final: ')
			for i in range(len(population)):
				print('['+population[i].toString() + '] - Fitness: '+ str(lastFitnessList[i]))
			print('Melhor gene:\n[' + population[lastBestGeneIndex].toString() +'] = '+ str(getElementValueAndFitness(population[lastBestGeneIndex])[0])+' - Fitness:'+ str(lastFitnessList[lastBestGeneIndex]))

		plotGraphs = readOption('\nDeseja ver o grafico com a media de desempenho e o melhor desempenho de cada geracao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(avgFitnessList))
			plt.plot(x,avgFitnessList, label="Average fitness")
			plt.plot(x,bestFitnessList, label="Best fitness")
			plt.ylabel('Fitness')
			plt.xlabel('Generation')
			plt.legend()
			plt.show()

		plotGraphs = readOption('\nDeseja ver o melhor ponto encontrado no graficoda funcao? (s/n)\n','s','n')

		if plotGraphs:
			plotPointOnCurve(bestGene)
elif algorithm == 2:
	print("\n------------------------------------------------")
	print('Subida de colina:\n')
	
	stringSize = readIntMin('Tamanho da bitstring que representa x: ', 2)

	maxIt = readIntMin('\nNumero maximo de iteracoes do algoritmo: ',1)
	maxNoImprove = readIntMin('Numero maximo de iteracoes sem melhora do algoritmo: ',1)
	
	multipleExecutions = readOption('\nDeseja executar diversas vezes com esse parametros para obter estatisticas? (s/n)\n','s','n')

	if multipleExecutions:
		n = readIntMin('Numero de execucoes do algoritmo: ', 1)
		itCountList = []
		itSolutionList = []
		itFitnnesList = []
		gotToLimitIt = 0
		nextPoint = 0
		print('\nExecutando...')
		start = time.time()			
		for i in range(n):
			x = BinaryString.newRandom(stringSize)			
			
			[bestX, bestFitness, achieved, bestFitnessList, fitnessList, generationCount] = hillClimbing(x, maxIt, maxNoImprove, disturbPlusOne, getElementFitness, newFitnessIsBetter, hillClimbingShouldStop)

			if generationCount >= maxIt:
				gotToLimitIt += 1

			itCountList.append(generationCount)
			itSolutionList.append(bestX)
			itFitnnesList.append(bestFitness)

			prct = float(i)/n
			if(prct >= nextPoint):
				pointTime = time.time()						
				print('['+secondsToString(pointTime - start)+'] - '+str(100*prct)+'%')
				nextPoint += 0.1


		end = time.time()
		elapsed = (end - start)*1000
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

		print('\nExecucoes que pararam por atingir o maximo de iteracoes: '+str(gotToLimitIt) + ' de '+str(n))

		plotGraphs = readOption('\nDeseja ver o grafico da quantidade de iteracoes para cada execucao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(itCountList))
			mean = len(x) * [avgItCount]
			plt.bar(x,itCountList)
			plt.plot(x,mean,'r-',label="Mean")
			plt.ylabel('Iterations')
			plt.xlabel('Execution')
			plt.legend()
			plt.show()

		plotGraphs = readOption('\nDeseja ver os pontos maximos encontrados na curva? (s/n)\n','s','n')

		if plotGraphs:
			px = []
			py = []
			for i in range(len(itSolutionList)):
				[val, gx] = getElementValueAndFitness(itSolutionList[i])
				px.append(val) 
				py.append(gx)
			x = []
			y = []
			for i in range(100):
				x.append(i * 0.01)
				y.append(g(x[i])) 
			plt.plot(x,y)
			plt.plot(px,py,'ro',label="Max points found")
			plt.ylabel('g(x)')
			plt.xlabel('x')
			plt.legend()
			plt.show()

	else:
		x = BinaryString.newRandom(stringSize)
			
		print('\nExecutando...')
		start = time.time()
		
		[bestX, bestFitness, achieved, bestFitnessList, fitnessList, generationCount] = hillClimbing(x, maxIt, maxNoImprove, disturbPlusOne, getElementFitness, newFitnessIsBetter, hillClimbingShouldStop)

		end = time.time()
		elapsed = (end - start)*1000
		print('Finalizado em '+str(elapsed)+'ms\n')

		print('Geracoes executadas: '+str(generationCount))
		bestGeneValue = getElementValueAndFitness(bestX)[0]
		print('Valor maximo atingido: g('+str(bestGeneValue)+')='+ str(bestFitness))

		plotGraphs = readOption('\nDeseja ver o grafico com o desempenho a cada iteracao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(fitnessList))
			plt.plot(x,fitnessList, label="Disturbed Fitness")
			plt.plot(x,bestFitnessList, label="Best Fitness")
			plt.legend()
			plt.ylabel('Fitness')
			plt.xlabel('Iteration')
			plt.legend()
			plt.show()
		
		plotGraphs = readOption('\nDeseja ver o melhor ponto encontrado no grafico da funcao? (s/n)\n','s','n')

		if plotGraphs:
			plotPointOnCurve(bestX)
elif algorithm == 3:
	print("\n------------------------------------------------")
	print('Recozimento simulado:\n')

	stringSize = readIntMin('Tamanho da bitstring que representa x: ', 2)

	maxIt = readIntMin('\nNumero maximo de iteracoes do algoritmo: ',1)
	maxNoImprove = readIntMin('Numero maximo de iteracoes sem melhora do algoritmo: ',1)
	initialTemperature = readFloat('Temperatura inicial do sistema: ')

	multipleExecutions = readOption('\nDeseja executar diversas vezes com esse parametros para obter estatisticas? (s/n)\n','s','n')

	if multipleExecutions:
		n = readIntMin('Numero de execucoes do algoritmo: ', 1)
		itCountList = []
		itSolutionList = []
		itFitnnesList = []
		gotToLimitIt = 0
		nextPoint = 0
		print('\nExecutando...')
		start = time.time()		

		for i in range(n):
			x = BinaryString.newRandom(stringSize)

			[bestX, bestFitness, achieved, bestFitnessList, fitnessList, generationCount] = simulatedAnnealing(x, maxIt, maxNoImprove, initialTemperature, disturbMutating, 
			getElementFitness, newFitnessIsBetter, lowerTemperature, simulatedAnnealingShouldStop)

			if generationCount >= maxIt:
				gotToLimitIt += 1

			itCountList.append(generationCount)
			itSolutionList.append(bestX)
			itFitnnesList.append(bestFitness)

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

		print('\nExecucoes que pararam por atingir o maximo de iteracoes: '+str(gotToLimitIt) + ' de '+str(n))


		plotGraphs = readOption('\nDeseja ver o grafico da quantidade de iteracoes para cada execucao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(itCountList))
			mean = len(x) * [avgItCount]
			plt.bar(x,itCountList)
			plt.plot(x,mean,'r-',label="Mean")
			plt.ylabel('Iterations')
			plt.xlabel('Execution')
			plt.legend()
			plt.show()

		plotGraphs = readOption('\nDeseja ver os pontos maximos encontrados na curva? (s/n)\n','s','n')

		if plotGraphs:
			px = []
			py = []
			for i in range(len(itSolutionList)):
				[val, gx] = getElementValueAndFitness(itSolutionList[i])
				px.append(val) 
				py.append(gx)
			x = []
			y = []
			for i in range(100):
				x.append(i * 0.01)
				y.append(g(x[i])) 
			plt.plot(x,y)
			plt.plot(px,py,'ro',label="Max points found")
			plt.ylabel('g(x)')
			plt.xlabel('x')
			plt.legend()
			plt.show()

	else:	
		x = BinaryString.newRandom(stringSize)
		print('\nExecutando...')
		start = time.time()

		[bestX, bestFitness, achieved, bestFitnessList, fitnessList, generationCount] = simulatedAnnealing(x, maxIt, maxNoImprove, initialTemperature, disturbMutating, getElementFitness, newFitnessIsBetter, lowerTemperature, simulatedAnnealingShouldStop)

		end = time.time()
		elapsed = (end - start)*1000
		print('Finalizado em '+str(elapsed)+'ms\n')

		print('Geracoes executadas: '+str(generationCount))
		bestGeneValue = getElementValueAndFitness(bestX)[0]
		print('Valor maximo atingido: g('+str(bestGeneValue)+')='+ str(bestFitness))

		plotGraphs = readOption('\nDeseja ver o grafico com o desempenho a cada iteracao? (s/n)\n','s','n')

		if plotGraphs:
			x = range(len(fitnessList))
			plt.plot(x,fitnessList, label="Iteration Fitness")
			plt.plot(x,bestFitnessList, label="Best Fitness")
			plt.ylabel('Fitness')
			plt.xlabel('Iteration')
			plt.legend()
			plt.show()
		
		plotGraphs = readOption('\nDeseja ver o melhor ponto encontrado no grafico da funcao? (s/n)\n','s','n')

		if plotGraphs:
			plotPointOnCurve(bestX)

print('\nFinalizando script...')
