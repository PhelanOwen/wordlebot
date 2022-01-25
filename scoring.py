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
		score = sum([self.STATS[letter] for letter in word])
		
		score *= len(set(word))  # unique letters score more
			
		if any(l in word for l in POTENT):
			score *= 1000  # potential letters score more
		if any(l in word for l in WRONG):
			return 0
		for i in range(len(word)):
			if word[i] not in current_guess.letters[i]:
				return 0

		return score