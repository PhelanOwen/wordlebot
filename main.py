import pickle
import random

STATS = {}
WORDS = [w.strip() for w in open('word_list.txt', 'r').readlines()]
WRONG = []
POTENT= []

class guessable_word:
    letters = [list('abcdefghijklmnopqrstuvwxyz') for i in range(0,5)]

def calculate_scores(picklefile):
    global STATS, WORDS
    STATS = {}
    words = WORDS
    for word in words:
        for letter in word:
            try:
                STATS[letter] += 1
            except:
                STATS[letter] = 1
    f = open(picklefile, 'wb')
    pickle.dump(STATS, f)
    f.close()
    
def load_stats(picklefile):
    global STATS
    f = open(picklefile, 'rb')
    STATS = pickle.load(f)
    f.close()

def get_word_score(word):
    global STATS, WRONG
    letters = list(word)
    score = sum([STATS[letter] for letter in letters])
    if len(set(letters)) == len(letters):  # score more if we pick words without duplicates
        score *= 2
    if any(l in word for l in POTENT):
        score *= 2
    if any(l in word for l in WRONG):
        score *= -1
    return score

def compare_word(actual, guess, current_known):
    global WRONG, POTENT
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
                WRONG.append(slots_guess[i])
        # letter is in word, but not in correct place
        if slots_guess[i] in slots and slots[i] != slots_guess[i]:
            try:
                current_known.letters[i].remove(slots_guess[i])
            except:
                pass
            POTENT.append(slots_guess[i])
        # letter is in correct place
        if slots_guess[i] == slots[i]:
            current_known.letters[i] = [slots_guess[i]]


test = "prime"

if __name__ == '__main__':
    guess_values = guessable_word()
    load_stats('scores')
    for i in range(0,6):
        WORDS = sorted(WORDS, key=lambda x: get_word_score(x), reverse=True)
        chosen = random.choice(WORDS[0: max(1, 5-(i*2))])
        print(chosen)
        compare_word(test, chosen, guess_values)