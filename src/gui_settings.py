# The settings file
settingsFile = 'src/data/settings.json'

# The program's name
programName = 'Casual Word Game'

# The program's version
programVersion = '2.0'

# Indicates how many letters to reveal from a word (0.5 means half of the letters, 0.3 one third of the letters
# etc.). Varies with the 'difficulty'
revealLettersRatio = {'Easy': 0.5, 'Medium': 0.5, 'Hard': 0.3}

# Controls the game's difficulty. Could be either 'Easy', 'Medium' (the default) or 'Hard'
difficulty = 'Medium'
difficultyOptions = ['Easy', 'Medium', 'Hard']

# The display name of the player
displayName = 'Player'

# The language of the game
language = 'EN'
languageOptions = ['En', 'Bg', 'De']

# Music on (True) or off (False)
music = 'On'
musicOptions = ['On', 'Off']

# SFX on (True) or off (False)
sfx = 'On'
sfxOptions = ['On', 'Off']

# Indicates the number of attempts to guess the word. The numbers mean 'add that many to the value of
# revealLettersRatio'. Example: On the 'Easy' setting if there are 3 letters revealed, one would have 5 (3 + 2)
# attempts to guess the word. Varies with the 'difficulty'
attempts = {'Easy': 2, 'Medium': 1, 'Hard': 0}

# Indicates the time available to guess the word. Varies with the 'difficulty'. Expressed in seconds
time = {'Easy': 181, 'Medium': 121, 'Hard': 61}
