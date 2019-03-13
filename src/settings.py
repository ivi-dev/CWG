import os

import sys

# The path to the active .py file
rootPath = os.path.split(sys.argv[0])[0]

# The settings file
settingsFile = os.path.join(rootPath, 'data', 'settings.json')

# The path to the images directory
imageDir = os.path.join(rootPath, 'data', 'images')

# The path to the sound directory
soundDir = os.path.join(rootPath, 'data', 'sound')

# The path to the data directory
dataDir = os.path.join(rootPath, 'data')

# The program's name
programName = 'Casual Word Game'

# The program's version
programVersion = '2.0'

# Helps to calculate how many incorrect attempts are available to guess the word. The calculation is made by
# multiplying the length of the word by the attemptsRatio. Varies with the 'difficulty'
attemptsRatio = {'Easy': 1, 'Medium': 0.5, 'Hard': 0.3}

# Indicates the number of attempts to guess the word. The numbers mean 'add that many to the value of
# revealLettersRatio'. Example: On the 'Easy' setting if there are 3 letters revealed, one would have 5 (3 + 2)
# attempts to guess the word. Varies with the 'difficulty'
attempts = {'Easy': 2, 'Medium': 0, 'Hard': -1}

# Controls the game's difficulty. Could be either 'Easy', 'Medium' (the default) or 'Hard'
difficultyOptions = ['Easy', 'Medium', 'Hard']
difficulty = difficultyOptions[1]

# The display name of the player
displayName = 'Player'

# The language of the game
languageOptions = ['En', 'Bg', 'De']
language = languageOptions[0]

# Music on (True) or off (False)
music = 'On'
musicOptions = ['On', 'Off']

# SFX on (True) or off (False)
sfx = 'On'
sfxOptions = ['On', 'Off']

# Indicates the time available to guess the word. Varies with the 'difficulty'. Expressed in seconds
time = {'Easy': 181, 'Medium': 121, 'Hard': 61}
