import random
# from matplotlib import pyplot as pp
from scoring import scoring
from wording import wording

STATS = {}
SIZE_BEFORE_COMMITTING = 3

class guessable_word:
	def __init__(self):
		self.letters = [list('abcdefghijklmnopqrstuvwxyz') for i in range(0,5)]

def compare_word(actual, guess, current_known, words):
	slots = list(actual)
	slots_guess = list(guess)
	for i in range(0,5):
		# Letter is not in actual word at all
		if slots_guess[i] not in actual:
			for possible in current_known.letters:
				try:
					possible.remove(slots_guess[i])
				except:  # got it right the first time
					pass
				words.WRONG.add(slots_guess[i])
		# letter is in word, but not in correct place
		elif slots_guess[i] in slots and slots[i] != slots_guess[i]:
			words.POTENT.add(slots_guess[i])
			try:
				current_known.letters[i].remove(slots_guess[i])
			except:
				pass
		# letter is in correct place
		elif slots_guess[i] == slots[i]:
			current_known.letters[i] = [slots_guess[i]]

def deduce_word(guess, result, current_known, words):
	for r in range(0,5):
		if result[r] == '1':
			current_known.letters[r] = [guess[r]]
		elif result[r] == '2':
			try:
				current_known.letters[r].remove(guess[r])
			except:
				pass
			words.POTENT.add(guess[r])
		else:
			for i in range(0,5):
				try:
					current_known.letters[i].remove(guess[r])
				except:
					pass
			words.WRONG.add(guess[r])

def pick_next_word(current_guess, words):
	
	for word in words.WORDS:
		usable = True  # assume the next word is usable
		
		if word in words.GUESSED:
			usable = False
			continue
		
		# Now we say that if we know a letter doesn't go somewhere
		# then we discard that word and try the next one
		for i, letter in enumerate(word):
			if letter not in current_guess.letters[i]:
				usable = False
				break
		
		if not usable:
			words.WORDS.remove(word)
		else:
			return word
			
	return random.choice(words.WORDS) # should only hit this if we've failed miserably

def run_sample(test_word, words, scoring):
	guess_values = guessable_word()
	scoring.load_stats('scores')
	chosen = ''
	for i in range(0,6):
		chosen = pick_next_word(guess_values, words)
		words.WORDS = sorted(words.WORDS, key=lambda x: scoring.get_word_score(x, guess_values, words.POTENT, words.WRONG), reverse=True)

		words.GUESSED.append(chosen)
		if chosen == test_word:
			print("** %s **" % chosen)
			return i+1
		
		compare_word(test_word, chosen, guess_values, words)
	print (chosen, test_word)
	return 7

def run_live():
	words = wording()
	scores = scoring()
	scores.load_stats('scores')
	guess_values = guessable_word()
	
	for i in range(6):
		words.WORDS = sorted(words.WORDS, key=lambda x: scores.get_word_score(x, guess_values, words.POTENT, words.WRONG), reverse=True)
		guess = pick_next_word(guess_values, words)
		print("Try this:", guess)
		result = input("[0=Grey][1=Green][2=Yellow]: ")
		if result == 'q':
			return 0
		deduce_word(guess, result, guess_values, words)
		words.GUESSED.append(guess)
		
		print()

def stat_run():
	res = []
	g = wording()
	s = scoring()
	for i in range(0,100):
		g.reset_guesses()
		res.append(run_sample(random.choice(g.WORDS), g, s))
	# pp.hist(res, len(set(res)))
	# pp.show()

if __name__ == '__main__':
	run_live()