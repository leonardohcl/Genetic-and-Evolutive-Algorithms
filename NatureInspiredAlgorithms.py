# encoding: utf-8
from BinaryString import BinaryString
from random import random, randint

def geneticAlgorithm(population, maxIt, select, breed, vary, avail, achievedTarget):
	it = 0
	avgFitness = []
	bestFitness = []

	#Enquanto não atingir o máximo de iterações e não chegar a aptidão alvo faça
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
	