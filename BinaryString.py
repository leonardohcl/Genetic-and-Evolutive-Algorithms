from random import randint
from random import random

class BinaryString:

	@staticmethod
	def rand(size):
		randList = []
		for i in range(size):
			randList.append(randint(0, 1))
		return BinaryString(randList)

	@staticmethod
	def toInt(binStr):
		if not isinstance(binStr, BinaryString):
			raise Exception('BinaryString.toInt parameter must be of type BinaryString')
		value = 0		
		for i in range(1, binStr.size):
			value += binStr.bin[i]*(2**+(binStr.size-i-1))
		if binStr.bin[0] == 1:
			value = value * -1
		return value

	
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

	def mutate(self, p):
		if p > 1 or p < 0:
			raise Exception('Mutation probability must be a value between 0 and 1 to represent a percentage')
		for i in range(self.size):
			if random() < p:
				if self.bin[i] == 0:
					self.bin[i] = 1
				else:
					self.bin[i] = 0
		self.decimal = BinaryString.toInt(self)

	def toString(self):
		string = ''
		for i in range(self.size):
			string += str(self.bin[i])
		return string

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
			self.decimal = BinaryString.toInt(self)
		else:
			raise Exception('Binary String value must be of type list')
