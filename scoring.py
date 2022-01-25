import pickle

class scoring:

	def __init__(self):
		self.STATS = {}

	def calculate_stats(self, picklefile, WORDS):
		self.STATS = {}
		words = WORDS
		for word in words:
			for letter in word:
				try:
					self.STATS[letter] += 1
				except:
					self.STATS[letter] = 1
		f = open(picklefile, 'wb')
		pickle.dump(self.STATS, f)
		f.close()
		
	def load_stats(self, picklefile):
		f = open(picklefile, 'rb')
		self.STATS = pickle.load(f)
		f.close()

	def get_word_score(self, word, current_guess, POTENT, WRONG):
		letters = list(word)
		score = sum([self.STATS[letter] for letter in letters])
		
		score *= len(set(letters))  # unique letters score more
			
		if any(l in letters for l in POTENT):
			score *= 5
		if any(l in letters for l in WRONG):
			score = 0
		for possibilities in current_guess.letters:
			if any(l not in possibilities for l in word):
				score = 0

		return score