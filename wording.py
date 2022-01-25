class wording:
	def __init__(self):
		self.reset_guesses()
	def reset_guesses(self):
		self.WRONG = set()
		self.POTENT = set()
		self.GUESSED = []
		self.WORDS = [w.strip() for w in open('word_list.txt', 'r').readlines()]