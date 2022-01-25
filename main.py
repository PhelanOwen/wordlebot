from operator import indexOf
import random
from matplotlib import pyplot as pp
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

def pick_next_word(current_guess, words):
	
	for word in words.WORDS:
		usable = True  # assume the next word is usable
		
		if word in words.GUESSED:
			usable = False
			continue
		
		# Now we say that if we know a letter doesn't go somewhere
		# then we discard that word and try the next one
		for i, letter in enumerate(word):
			if len(words.POTENT) < 2:
				if letter in words.POTENT:
					usable = False
					continue

			elif letter not in current_guess.letters[i]:
				usable = False
				continue
		
		if not usable:
			words.WORDS.remove(word)
		else:
			return word
			
	return words.WORDS[0] # should only hit this if we've failed miserably

def run_sample(test_word, words, scoring):
	guess_values = guessable_word()
	scoring.load_stats('scores')
	chosen = ''
	for i in range(0,20):
		if i == 0:
			chosen = 'adieu'
		else:
			chosen = pick_next_word(guess_values, words)
			words.WORDS = sorted(words.WORDS, key=lambda x: scoring.get_word_score(x, guess_values, words.POTENT, words.WRONG), reverse=True)

		words.GUESSED.append(chosen)
		if chosen == test_word:
			print("** %s **" %chosen)
			return i+1
		
		compare_word(test_word, chosen, guess_values, words)
	print (chosen, test_word)
	return 7

if __name__ == '__main__':
	res = []
	g = wording()
	s = scoring()
	for i in range(0,1000):
		g.reset_guesses()
		res.append(run_sample(random.choice(g.WORDS), g, s))
	pp.hist(res, len(set(res)))
	pp.show()