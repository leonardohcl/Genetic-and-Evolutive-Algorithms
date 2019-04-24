# encoding: utf-8
from BinaryString import BinaryString
from random import random, randint
from math import exp

def geneticAlgorithm(population, maxIt, select, breed, vary, avail, achievedTarget):
	it = 0
	avgFitness = []
	bestFitness = []

	#Enquanto não atingir o máximo de iterações
	while it <= maxIt:
		#Avalia a população
		[fitnessList, bestGeneIndex]= avail(population)

		#Registra o fitness médio e o melhor da população
		bestFitness.append(fitnessList[bestGeneIndex])
		itAvgFitness = sum(fitnessList)/len(fitnessList)
		avgFitness.append(itAvgFitness)

		#Se atingiu o objetivo para as iterações
		if(achievedTarget(fitnessList, bestGeneIndex)):
			break

		#Seleciona a população da próxima geração
		population = select(population, fitnessList)
		
		#Cruza a população
		population = breed(population, fitnessList)

		#Varia a população
		population = vary(population)

		#Incrementa a iteração
		it += 1
	
	return [population, fitnessList, bestGeneIndex, it, avgFitness, bestFitness]

def hillClimbing(x, maxIt, maxNoImprove, disturb, avail, shouldGetTheDisturbed, achievedTarget):
	it = 0
	noImprove = 0
	#Avalia x
	bestFitness = avail(x)
	fitness = [bestFitness]
	achieved = False	
	#Enquanto não atingir o máximo de iterações
	while it < maxIt:
		#Se atingiu o objetivo para as iteracoes
		if achievedTarget(bestFitness):
			achieved = True
			break

		#Perturba x
		aux = disturb(x)
		auxFitness = avail(x)

		#Verifica se deve substituir x por x'
		if(shouldGetTheDisturbed(bestFitness,auxFitness)):
			x = aux
			bestFitness = auxFitness
			noImprove = 0
		else:
			noImprove += 1

		fitness.append(bestFitness)

		#Se atingiu o máximo de iterações sem melhorar para as iterações			
		if noImprove >= maxNoImprove:
			break
		
		it += 1

	return [x, bestFitness, achieved, fitness, it]

def iterativeHillClimbing(initialX, maxHillClimbingIterations, maxIt, maxNoImprove, disturb, avail, shouldGetTheDisturbed, achievedTarget):
	it = 0
	x = initialX
	bestX = x
	bestFitness = avail(x)
	fitness = [bestFitness]
	achieved = False
	#Enquanto não atingir o máximo de iterações do Hill Climbing	
	while it < maxHillClimbingIterations:
		#Se atingiu o objetivo para as iteracoes
		if achievedTarget(bestFitness):
			achieved = True
			break

		it += 1

		#Gera um x aleatório
		x = BinaryString.newRandom(initialX.size)
		
		#Executa o hill climbing pro x gerado
		[x, iterationFitness, itHcAchieved, fitnessList, itHcIterations] = hillClimbing(x, maxIt, maxNoImprove, disturb, avail, shouldGetTheDisturbed, achievedTarget)
		

		#Se x'for melhor que x substitui os valores
		if(shouldGetTheDisturbed(bestFitness,iterationFitness)):
			bestX = x
			bestFitness = iterationFitness

		fitness.append(bestFitness)

	return [bestX, bestFitness, achieved, fitness, it]

def simulatedAnnealing(x, maxIt, maxNoImprove, initialTemperature, disturb, avail, shouldGetTheDisturbed, temperatureChange, achievedTarget):
	temperature = initialTemperature
	it = 0
	noImprove = 0
	#Avalia x
	bestFitness = avail(x)
	fitness = [bestFitness]
	achieved = False	
	#Enquanto não atingir o máximo de iterações
	while it < maxIt:
		#Se atingiu o objetivo para as iteracoes
		if achievedTarget(bestFitness):
			achieved = True
			break

		#Perturba x
		aux = disturb(x)
		auxFitness = avail(x)

		#Verifica se deve substituir x por x'
		if(shouldGetTheDisturbed(bestFitness,auxFitness)):
			x = aux
			bestFitness = auxFitness
			noImprove = 0
		else:
			probability = exp((float(-abs(bestFitness-auxFitness))/temperature))
			if random() <= probability:
				x = aux
				bestFitness = auxFitness
			else:
				noImprove += 1


		fitness.append(bestFitness)

		#Se atingiu o máximo de iterações sem melhorar para as iterações			
		if noImprove >= maxNoImprove:
			break

		it += 1
		temperature = temperatureChange(temperature,it)					

	return [x, bestFitness, achieved, fitness, it]
