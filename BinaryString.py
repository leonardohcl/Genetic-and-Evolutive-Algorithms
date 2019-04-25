from random import randint
from random import random

class BinaryString:

	@staticmethod
	def newRandom(size):
		randList = []
		for i in range(size):
			randList.append(randint(0, 1))
		return BinaryString(randList)
	
	@staticmethod
	def newFromInt(n):
		if not isinstance(n, int) :
			raise Exception('BinaryString.newFromInt parameter must be of type int')
		aux = [] 
		if n < 0:
			sign = [1]
		else:
			sign = [0]
		n = abs(n)	
		while n > 0:
			aux = [n%2] + aux
			n = n/2
		aux = sign + aux
		return BinaryString(aux)

	@staticmethod
	def hammingDistance(binStr1, binStr2):
		if binStr1.size != binStr2.size:
			 raise Exception('The Hamming distance can only be calculated for Binary Strings of the same size')
		distance = 0
		for i in range(binStr1.size):
			if binStr1.bin[i] != binStr2.bin[i]:
				distance += 1
		return distance
	
	@staticmethod
	def crossover(binStr1, binStr2, point):
		if binStr1.size != binStr2.size:
			raise Exception('You can only crossover Binary Strings of the same size')		
		if point >= binStr1.size:
			raise Exception('You can\'t crossover on a point that\'s larger than the Binary String size')
		newBinStr1 = binStr1.bin[0:point] + binStr2.bin[point:binStr2.size]
		newBinStr2 = binStr2.bin[0:point] + binStr1.bin[point:binStr1.size]
		return [BinaryString(newBinStr1), BinaryString(newBinStr2)]

	@staticmethod
	def changeSize(binStr,size):
		if size < 2:
			raise Exception('A binary string must be at least size 2')

		sizeDiff = binStr.size - size		
		if sizeDiff > 0:
			newBin = [binStr.bin[0]] + binStr.bin[sizeDiff+1:]
		elif sizeDiff < 0:
			sizeDiff = abs(sizeDiff)
			newBin = [binStr.bin[0]] + (sizeDiff*[0]) + binStr.bin[1:]
		else:
			newBin = binStr.bin
		return BinaryString(newBin)


	def mutate(self, p):
		if p > 1 or p < 0:
			raise Exception('Mutation probability must be a value between 0 and 1 to represent a percentage')
		for i in range(self.size):
			if random() < p:
				if self.bin[i] == 0:
					self.bin[i] = 1
				else:
					self.bin[i] = 0

	def toString(self):
		string = ''
		for i in range(self.size):
			string += str(self.bin[i])
		return string

	def binToInt(self):
		value = 0		
		for i in range(1, self.size):
			value += self.bin[i]*(2**+(self.size-i-1))
		if self.bin[0] == 1:
			value = value * -1
		return value

	# Constructor
	def __init__(self, binStr):
		if isinstance(binStr, list):
			for i in binStr:
				if not isinstance(i, int):
					raise Exception('Binary String list values must be of type int')
				if i < 0 or i > 1:
					raise Exception('Binary String list values must be only 0 or 1')
			self.bin = list(binStr)			
			self.size = len(self.bin)
		else:
			raise Exception('Binary String value must be of type list')
