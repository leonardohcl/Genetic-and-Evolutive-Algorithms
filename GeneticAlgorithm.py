# encoding: utf-8
from BinaryString import BinaryString
from random import random, randint
from copy import deepcopy

class Crossover:
	def __init__(self, should, probability, rangeStart, rangeEnd, cross):
		if(rangeStart > rangeEnd):
			raise Exception('Crossover range start must be smaller than the end')
		self.should = should
		self.probability = probability
		self.rangeStart = rangeStart
		self.rangeEnd = rangeEnd
		self.cross = cross

class Mutation:
	def __init__(self, should, probability):
		if probability > 1 or probability < 0:
			raise Exception('Mutation probability must be between 0 and 1')
		self.should = should
		self.probability = probability


def geneticAlgorithm(population, maxIt, crossoverSettings, mutationSettings, targetFitnessAchieved, fitnessCalculation, getBestFitness):
	it = 0
	avgFitness = []
	bestFitness = []
	#Enquanto não atingir o máximo de iterações e não chegar a aptidão alvo faça
	while it <= maxIt:
		fitnessList = []
		populationAvgFitness = 0
		#Para cada individuo na população
		for i in range(len(population)):
			#Calcular a aptidão
			fitnessList.append(fitnessCalculation(population[i]))
			populationAvgFitness += fitnessList[i]
		
		#Calcula a aptidão média da geração
		populationAvgFitness = populationAvgFitness / float(len(population))
		avgFitness.append(populationAvgFitness)

		#Encontra o melhor gene da geração
		[bestItFitness, bestItFitnessIndex] = getBestFitness(fitnessList)
		bestFitness.append(bestItFitness)

		#Se a aptidao for a esperada
		if(targetFitnessAchieved(bestItFitness, population)):
			#Para as iteracoes do algoritmo
			break

		#Faz crossover (se configurado para isso)
		if crossoverSettings.should:
			population = crossoverSettings.cross(population, fitnessList, crossoverSettings)
			
			
		#Aplica mutação (se configurado para isso)
		if mutationSettings.should:
			for i in range(len(population)):
				population[i].mutate(mutationSettings.probability)

		#Incrementa o contador de iteracao
		it += 1
	
	return [population, fitnessList, it, avgFitness, bestFitness, bestItFitnessIndex]

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

def crossover2by2(population, fitnessList, settings):
	#Seleciona os algoritmos para a nova populacao
	newPopulation = rouletteWheelSelection(population, fitnessList)

	#Faz o cruzamento dos indivíduos
	for i in range(0, len(population), 2):
		#Testa para ver se o par deve ser cruzado
		shouldCross = random() <= settings.probability
		#Se sim cruza os dois
		if shouldCross:
			point = randint(settings.rangeStart,settings.rangeEnd)
			[newPopulation[i],newPopulation[i+1]] = BinaryString.crossover(population[i],population[i+1],point)
	
	return newPopulation
