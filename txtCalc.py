# txtCalc - A text-based calculator
# Run => #python txtCalc.py 
#
# Author: Tarek Amr (@gr33ndata)
# Date: January 2012
#


expr = "ninety divided by 0"

C_NUM = 1
C_OP = 0
C_OP_NEG = -1
C_OP_NOP =  0
C_OP_ADD =  1
C_OP_SUB =  2
C_OP_MUL =  3
C_OP_DIV =  4

class Calculator:
	def __init__(self, debug=False):
		#print "Loading calculator"
		self.debug = debug
		self.expr = []
		self.dict = {
			"zero": {"type": C_NUM, "val": 0},
			"0": {"type": C_NUM, "val": 0},
			"one": {"type": C_NUM, "val": 1},
			"1": {"type": C_NUM, "val": 1},
			"two": {"type": C_NUM, "val": 2},
			"2": {"type": C_NUM, "val": 2},
			"three": {"type": C_NUM, "val": 3},
			"3": {"type": C_NUM, "val": 3},
			"four": {"type": C_NUM, "val": 4},
			"4": {"type": C_NUM, "val": 4},
			"five": {"type": C_NUM, "val": 5},
			"5": {"type": C_NUM, "val": 5},
			"six": {"type": C_NUM, "val": 6},
			"6": {"type": C_NUM, "val": 6},
			"seven": {"type": C_NUM, "val": 7},
			"7": {"type": C_NUM, "val": 7},
			"eight": {"type": C_NUM, "val": 8},
			"8": {"type": C_NUM, "val": 8},
			"nine": {"type": C_NUM, "val": 9},
			"9": {"type": C_NUM, "val": 9},
			"ten": {"type": C_NUM, "val": 10},
			"10": {"type": C_NUM, "val": 10},
			"eleven": {"type": C_NUM, "val": 11},
			"11": {"type": C_NUM, "val": 11},
			"twelve": {"type": C_NUM, "val": 12},
			"12": {"type": C_NUM, "val": 12},
			"thirteen": {"type": C_NUM, "val": 13},
			"13": {"type": C_NUM, "val": 13},
			"fourteen": {"type": C_NUM, "val": 14},
			"14": {"type": C_NUM, "val": 14},
			"fifteen": {"type": C_NUM, "val": 15},
			"15": {"type": C_NUM, "val": 15},
			"sixteen": {"type": C_NUM, "val": 16},
			"16": {"type": C_NUM, "val": 16},
			"serventeen": {"type": C_NUM, "val": 17},
			"17": {"type": C_NUM, "val": 17},
			"eighteen": {"type": C_NUM, "val": 18},
			"18": {"type": C_NUM, "val": 18},
			"nineteen": {"type": C_NUM, "val": 19},
			"19": {"type": C_NUM, "val": 19},
			"twenty": {"type": C_NUM, "val": 20},
			"20": {"type": C_NUM, "val": 20},
			"thirty": {"type": C_NUM, "val": 30},
			"30": {"type": C_NUM, "val": 30},
			"fourty": {"type": C_NUM, "val": 40},
			"40": {"type": C_NUM, "val": 40},
			"fifty": {"type": C_NUM, "val": 50},
			"50": {"type": C_NUM, "val": 50},
			"sixty": {"type": C_NUM, "val": 60},
			"60": {"type": C_NUM, "val": 60},
			"seventy": {"type": C_NUM, "val": 70},
			"70": {"type": C_NUM, "val": 70},
			"eighty": {"type": C_NUM, "val": 80},
			"80": {"type": C_NUM, "val": 80},
			"ninety": {"type": C_NUM, "val": 90},
			"90": {"type": C_NUM, "val": 90},
			"hundred": {"type": C_NUM, "val": 100},
			"100": {"type": C_NUM, "val": 100},
			"thousand": {"type": C_NUM, "val": 1000},
			"1000": {"type": C_NUM, "val": 1000},
			"million": {"type": C_NUM, "val": 1000000},
			"1000000": {"type": C_NUM, "val": 1000000},
			"plus": {"type": C_OP, "val": C_OP_ADD},
			"+": {"type": C_OP, "val": C_OP_ADD},
			"minus": {"type": C_OP, "val": C_OP_SUB},
			"-": {"type": C_OP, "val": C_OP_SUB},
			"times": {"type": C_OP, "val": C_OP_MUL},
			"*": {"type": C_OP, "val": C_OP_MUL},
			"divided": {"type": C_OP, "val": C_OP_DIV},
			"by": {"type": C_OP, "val": C_OP_NOP},
			"/": {"type": C_OP, "val": C_OP_DIV},
			"and": {"type": C_OP, "val": C_OP_NOP},
			"negative": {"type": C_OP, "val": C_OP_NEG},
		}
	
	def print_debug(self, msg):
		if self.debug == True:
			print msg
			
	def tokenize(self, expr_str):
		try:
			return expr_str.split(" ")
		except:
			return []
	
	""" Normalize
	This method is respnosible for stuff like:
	three hundred and two -> 3 x 100 + 2
	negative twenty three -> -1 x (20 + 3)
	"""
	def normalize(self, expr_nums):
		#self.print_debug("Starting normalization: %s" % expr_nums)
		if expr_nums.__len__() == 0:
			return 0
		# For negative numbers, multiply by -1
		if expr_nums[0]["type"] == C_OP and expr_nums[0]["val"] == C_OP_NEG:
			return -1 * self.normalize(expr_nums[1:])
		# Skip stuff like and in one hundred and two, and by in divided by
		if expr_nums[0]["type"] == C_OP and expr_nums[0]["val"] == C_OP_NOP:
			return self.normalize(expr_nums[1:])
		# Number consisting of one word. Eg: one, 2, twenty
		if expr_nums[0]["type"] == C_NUM and expr_nums.__len__() == 1:
			return expr_nums[0]["val"]
		# Number like twenty tow (20 + 2) 
		if expr_nums[0]["type"] == C_NUM and expr_nums[0]["val"] > expr_nums[1]["val"]:
			return expr_nums[0]["val"] + self.normalize(expr_nums[1:])
		# Number like two hundred (2 X 100)
		if expr_nums[0]["type"] == C_NUM and expr_nums[0]["val"] < expr_nums[1]["val"]:
			return expr_nums[0]["val"] * expr_nums[1]["val"] + self.normalize(expr_nums[2:])
		
	""" Mul_Div
	We move from left to right multiply/divide parts of expression
	We then call Normalize for remaining sub-expressions
	"""	
	def mul_div(self, expr_muldiv):
		#self.print_debug("Starting add subtract: %s" % expr_addsub)
		for i in range(0,expr_muldiv.__len__()):
			if expr_muldiv[i]["type"] == C_OP and expr_muldiv[i]["val"] == C_OP_MUL:
				return self.mul_div(expr_muldiv[:i]) *  self.mul_div(expr_muldiv[i+1:])
			if expr_muldiv[i]["type"] == C_OP and expr_muldiv[i]["val"] == C_OP_DIV:
				return self.mul_div(expr_muldiv[:i]) /  self.mul_div(expr_muldiv[i+1:])
		return self.normalize(expr_muldiv)
	
	""" Add_Sub
	We move from left to right add/sub parts of expression
	We then call Multiply and Division for remaining sub-expressions
	"""
	def add_sub(self, expr_addsub):
		#self.print_debug("Starting add subtract: %s" % expr_addsub)
		for i in range(0,expr_addsub.__len__()):
			if expr_addsub[i]["type"] == C_OP and expr_addsub[i]["val"] == C_OP_ADD:
				return self.add_sub(expr_addsub[:i]) +  self.add_sub(expr_addsub[i+1:])
			if expr_addsub[i]["type"] == C_OP and expr_addsub[i]["val"] == C_OP_SUB:
				return self.add_sub(expr_addsub[:i]) -  self.add_sub(expr_addsub[i+1:])
		return self.mul_div(expr_addsub)
	
	""" Translate
	We use dictionary built in __init__ to transform text to numbers and expression
	We also make our expression case insensitive and add spaces between operations and numbers
	"""
	def translate(self, expr_str):
		expr_str = expr_str.lower().replace("+"," + ").replace("-"," - ").replace("*"," * ").replace("/"," / ")
		tokenized = self.tokenize(expr_str.lower())
		if not tokenized:
			raise Exception
		for item in tokenized:
			item = item.strip()
			if item:
				try:
					self.expr.append(self.dict[item])
				except KeyError:
					try:
						self.expr.append({"type": C_NUM, "val": int(item)})
					except:	
						raise
	
	""" Calculate
	This is the main function in our class
	It takes expression, calls translation for text to numbers conversion
	Then starts the calculations, starting with + & - as they take higher precidence than * & /
	"""
	def calculate(self, expr_str):
		#self.print_debug("Input: %s" % expr_str)
		try:
			self.translate(expr_str)
			res = self.add_sub(self.expr)
		except:
			res = "ERROR"
		self.expr = []
		print "Result: ", res
		return 0

	
if __name__ == "__main__":
	expressions = []
	c = Calculator(debug=True)
	print "Calculator v 1.0.0"
	print "Print enter your expression, one per line."
	print "Enter empty line to terminate"
	while True:
		expr = raw_input()
		if not expr:
			break
		expressions.append(expr)
	for item in expressions:
		trans = c.calculate(item)
	print ""
	

	