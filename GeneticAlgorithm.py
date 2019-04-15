# encoding: utf-8
from BinaryString import BinaryString
from random import random, randint
from copy import deepcopy
import matplotlib.pyplot as plt

class Crossover:
	def __init__(self, should, probability, rangeStart, rangeEnd, selection):
		if(rangeStart > rangeEnd):
			raise Exception('Crossover range start must be smaller than the end')
		self.should = should
		self.probability = probability
		self.rangeStart = rangeStart
		self.rangeEnd = rangeEnd
		self.selection = selection

class Mutation:
	def __init__(self, should, probability):
		if probability > 1 or probability < 0:
			raise Exception('Mutation probability must be between 0 and 1')
		self.should = should
		self.probability = probability


def geneticAlgorithm(population, maxIt, crossoverSettings, mutationSettings, targetFitness, fitnessCalculation, getBestFitness):
	it = 0
	bestFitness = targetFitness - 1
	avgFitness = []
	bestFitness = []
	#Enquanto não atingir o máximo de iterações e não chegar a aptidão alvo faça
	while it <= maxIt and bestFitness != targetFitness:
		# print('Geracao '+str(it))
		# print('Populacao:')
		fitnessList = []
		populationAvgFitness = 0
		#Para cada gene na população
		for i in range(len(population)):
			# print(population[i].bin)
			#Calcular a aptidão
			fitnessList.append(fitnessCalculation(population[i]))
			populationAvgFitness += fitnessList[i]
		
		#Calcula a aptidão média da geração
		populationAvgFitness = populationAvgFitness / float(len(population))
		avgFitness.append(populationAvgFitness)

		#Encontra o melhor gene da geração
		[bestItFitness, bestItFitnessIndex] = getBestFitness(fitnessList)
		bestFitness.append(bestItFitness)
		# print('Best gene: ')
		# print(population[bestItFitnessIndex].bin)
		# print('Fitness: '+str(bestItFitness))

		#Faz crossover (se configurado para isso)
		if crossoverSettings.should:
			#Seleciona os individuos para a próxima geração
			population = crossoverSettings.selection(population, fitnessList)

			#Faz o cruzamento dos indivíduos
			for i in range(0, len(population), 2):
				shouldCross = random() <= crossoverSettings.probability
				if shouldCross:
					point = randint(crossoverSettings.rangeStart,crossoverSettings.rangeEnd)
					[population[i],population[i+1]] = BinaryString.crossover(population[i],population[i+1],point)
			
		#Aplica mutação (se configurado para isso)
		if mutationSettings.should:
			for i in range(len(population)):
				population[i].mutate(mutationSettings.probability)

		it += 1
	
	x = range(len(avgFitness))
	plt.plot(x,avgFitness, label="avg")
	plt.plot(x,bestFitness, label="best")
	plt.legend()
	plt.show()
	return True

def rouletteWheelSelection(population, fitnessList):
	if(len(population) != len(fitnessList)):
		raise Exception("Population and fitness list must be the same length")

	wheelSections = []
	selectedGenes = []
	newPopulation = []
	totalFitness = sum(fitnessList)

	#Definição das seções da roda e sorteio de valor para nova população
	for i in range(len(fitnessList)):
		wheelSections.append(360*fitnessList[i] / float(totalFitness))
		selectedGenes.append(random() * 360)
		if i > 0:
			wheelSections[i] = wheelSections[i-1] + wheelSections[i]
	
	#Definição dos individuos sorteados
	for i in range(len(selectedGenes)):
		j = 0
		while j < len(wheelSections) and wheelSections[j] <= selectedGenes[i]:
			j+=1
		newPopulation.append(deepcopy(population[j]))

	return newPopulation
		