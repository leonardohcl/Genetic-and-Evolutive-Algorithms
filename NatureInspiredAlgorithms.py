# encoding: utf-8
from BinaryString import BinaryString
from random import random, randint
from math import exp

def geneticAlgorithm(population, maxIt, select, breed, vary, avail, achievedTarget, newFitnessIsBetter, maxItNoImprove = -1):
	it = 0
	avgFitnessList = []
	bestFitnessList = []
	noImproveIt = 0 
	bestFitness = 0
	bestGene = population[0]
	#Enquanto não atingir o máximo de iterações
	while it <= maxIt:
		#Avalia a população
		[fitnessList, bestGeneIndex]= avail(population)

		#Registra o fitness médio e o melhor da população
		bestFitnessList.append(fitnessList[bestGeneIndex])
		itAvgFitness = sum(fitnessList)/len(fitnessList)
		avgFitnessList.append(itAvgFitness)

		#Se for a primeira iteracao salva o melhor valor
		if it == 0:
			bestFitness = fitnessList[bestGeneIndex]
		#Senão verifica se o melhor valor mudou
		else:
			if(newFitnessIsBetter(bestFitness, fitnessList[bestGeneIndex])):
				bestFitness = fitnessList[bestGeneIndex]
				bestGene = population[bestGeneIndex]
				noImproveIt = 0
			else:
				noImproveIt += 1

		#Se atingiu o objetivo para as iterações
		if achievedTarget(fitnessList, bestGeneIndex):
			break

		if maxItNoImprove>=0 and noImproveIt >= maxItNoImprove:
			break

		#Seleciona a população da próxima geração
		population = select(population, fitnessList)
		
		#Cruza a população
		population = breed(population, fitnessList)

		#Varia a população
		population = vary(population)

		#Incrementa a iteração
		it += 1

	lastFitnessList = fitnessList
	lastBestGeneIndex = bestGeneIndex
	return [population, bestGene, bestFitness, lastFitnessList, lastBestGeneIndex, it, avgFitnessList, bestFitnessList]

def hillClimbing(x, maxIt, maxNoImprove, disturb, avail, shouldGetTheDisturbed, achievedTarget):
	it = 0
	noImprove = 0
	#Avalia x
	bestFitness = avail(x)
	bestFitnessList = [bestFitness]
	fitnessList = [bestFitness]
	achieved = False	
	#Enquanto não atingir o máximo de iterações
	while it < maxIt:
		#Se atingiu o objetivo para as iteracoes
		if achievedTarget(bestFitness):
			achieved = True
			break
		
		#Perturba x
		aux = disturb(x)
		auxFitness = avail(aux)

		#Verifica se deve substituir x por x'
		if(shouldGetTheDisturbed(bestFitness,auxFitness)):
			x = aux
			bestFitness = auxFitness
			noImprove = 0
		else:
			noImprove += 1

		fitnessList.append(auxFitness)
		bestFitnessList.append(bestFitness)
		#Se atingiu o máximo de iterações sem melhorar para as iterações			
		if noImprove >= maxNoImprove:
			break
		
		it += 1

	return [x, bestFitness, achieved, bestFitnessList, fitnessList, it]

def simulatedAnnealing(x, maxIt, maxNoImprove, initialTemperature, disturb, avail, shouldGetTheDisturbed, temperatureChange, achievedTarget):
	temperature = initialTemperature
	it = 0
	noImprove = 0
	#Avalia x
	bestFitness = avail(x)
	xFitness = bestFitness
	bestX = x
	fitnessList = [bestFitness]
	bestFitnessList = [bestFitness]
	achieved = False	
	#Enquanto não atingir o máximo de iterações
	while it < maxIt:
		#Se atingiu o objetivo para as iteracoes
		if achievedTarget(bestFitness):
			achieved = True
			break

		#Perturba x
		aux = disturb(x)
		auxFitness = avail(aux)


		#Verifica se deve substituir x por x'
		if(shouldGetTheDisturbed(bestFitness,auxFitness)):
			x = aux
			bestX = aux
			bestFitness = auxFitness
			xFitness = auxFitness
			noImprove = 0
		else:
			changeProbability = exp((float(-abs(bestFitness-auxFitness))/temperature))
			test = random()
			if test <= changeProbability:
				x = aux
				xFitness = auxFitness
			else:
				noImprove += 1

		fitnessList.append(xFitness)
		bestFitnessList.append(bestFitness)


		#Se atingiu o máximo de iterações sem melhorar para as iterações			
		if noImprove >= maxNoImprove:
			break

		it += 1
		temperature = temperatureChange(temperature,it)					

	return [bestX, bestFitness, achieved, bestFitnessList, fitnessList, it]
