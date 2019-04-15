def readFloat(msg):
	while True:
		try:
			value = float(input(msg))
			return value
		except:
			print('Valor invalido!')

def readFloatInterval(msg, start, end):
	if end < start:
		raise Exception("Interval start must be smaller than the end")
	while True:
		try:
			value = float(input(msg))
			if value < start or value > end:
				print('O valor deve estar contido no intervalo ['+str(start)+','+str(end)+'].')
			else:
				return value
		except:
			print('Valor invalido!')

def readFloatMax(msg, top):
	while True:
		try:
			value = float(input(msg))
			if value > top:
				print('O valor deve ser menor ou igual a '+str(top)+'.')
			else:
				return value
		except:
			print('Valor invalido!')

def readFloatMin(msg, bottom):
	while True:
		try:
			value = float(input(msg))
			if value < bottom:
				print('O valor deve ser maior ou igual a '+str(bottom)+'.')
			else:
				return value
		except:
			print('Valor invalido!')

def readInt(msg):
	while True:
		try:
			value = int(input(msg))
			return value
		except:
			print('Valor invalido!')

def readIntInterval(msg, start, end):
	if end < start:
		raise Exception("Interval start must be smaller than the end")
	while True:
		try:
			value = int(input(msg))
			if value < start or value > end:
				print('O valor deve estar contido no intervalo ['+str(start)+','+str(end)+'].')
			else:
				return value
		except:
			print('Valor invalido!')

def readIntMax(msg, top):
	while True:
		try:
			value = int(input(msg))
			if value > top:
				print('O valor deve ser menor ou igual a '+str(top)+'.')
			else:
				return value
		except:
			print('Valor invalido!')

def readIntMin(msg, bottom):
	while True:
		try:
			value = int(input(msg))
			if value < bottom:
				print('O valor deve ser maior ou igual a '+str(bottom)+'.')
			else:
				return value
		except:
			print('Valor invalido!')
	return value

def readOption(msg, trueValue, falseValue):
	while True:
		try:
			value = raw_input(msg)
			if value == trueValue:
				return True
			elif value == falseValue:
				return False
			else:
				print("Valor deve ser '"+str(trueValue)+"' ou '"+str(falseValue)+"'!")
			
		except:
			print('Valor invalido!')