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
	def binaryAdd(binStr1, binStr2, allowCarry):
		if not isinstance(binStr1, BinaryString) or not isinstance(binStr2, BinaryString):
			raise Exception('BinaryString.binaryAdd parameters must be both of type BinaryString')

		sizeDiff = abs(binStr1.size - binStr2.size)
		if sizeDiff > 0:
			if binStr1.size > binStr2.size:
				bin1 = binStr1.bin
				bin2 = (sizeDiff * [0]) + binStr2.bin
			else:				
				bin1 = (sizeDiff * [0]) + binStr1.bin
				bin2 = binStr2.bin
		else:
			bin1 = binStr1.bin
			bin2 = binStr2.bin

		carry = 0
		result = len(bin1) * [0]			
		for i in range(len(bin1)-1,-1,-1):
			if bin1[i] == 1:
				if bin2[i] == 1:
					if carry == 1:
						result[i] = 1
						carry = 1
					else:
						result[i] = 0
						carry = 1
				else:
					if carry == 1:
						result[i] = 0
						carry = 1
					else:
						result[i] = 1
						carry = 0
			else:
				if bin2[i] == 1:
					if carry == 1:
						result[i] = 0
						carry = 1
					else:
						result[i] = 1
						carry = 0
				else:
					if carry == 1:
						result[i] = 1
						carry = 0
					else:	
						result[i] = 0
						carry = 0
		
		if carry == 1 and allowCarry:
			result = [1] + result

		return BinaryString(result)

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
