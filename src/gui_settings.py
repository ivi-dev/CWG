# The program's name
programName = 'Casual Word Game'

# The program's version
programVersion = '2.0'

# Indicates how many letters to reveal from a word (0.5 means half of the letters, 0.3 one third of the letters
# etc.). Varies with the 'difficulty'
revealLettersRatio = {'easy': 0.5, 'medium': 0.5, 'hard': 0.3}

# Controls the game's difficulty. Could be either 'easy', 'medium' (the default) or 'hard'
difficulty = 'medium'

# Indicates the number of attempts to guess the word. The numbers mean 'add that many to the value of
# revealLettersRatio'. Example: On the 'easy' setting if there are 3 letters revealed, one would have 5 (3 + 2)
# attempts to guess the word. Varies with the 'difficulty'
attempts = {'easy': 2, 'medium': 1, 'hard': 0}

# Indicates the time available to guess the word. Varies with the 'difficulty'. Expressed in seconds
time = {'easy': 181, 'medium': 121, 'hard': 61}
