# The text for the labels in the info area
infoLabels = [('ATTEMPTS', 'attempts'), ('SYNONYMS', 'synonyms'), ('PART OF SPEECH', 'partOfSpeech')]

# The text for the labels in the settings
settingsLabels = [('DIFFICULTY', 'settings_difficulty', 'difficulty'),
                  ('LANGUAGE', 'settings_language', 'language'), ('MUSIC', 'settings_music', 'music'),
                  ('SOUND FX', 'settings_sound_fx', 'sfx')]

# The labels of the buttons. These hint to the code what image filename to choose for each button
buttonLabels = ['skip', '+a', 'settings', 'exit']

# The labels of the buttons. These hint to the code what image filename to choose for each button
settingsButtonLabels = ['apply', 'back']

# A collection of images from the UI. Keeps references to make sure that images are displayed
images = []

# The collection of words, typically loaded from a JSON file
wordsDB = {}

# The word of the game
word = {}

# Handles to canvas elements
canvasElements = {
    'wordDef': None,
    'letters': [],
    'attempts': None,
    'synonyms': None,
    'partOfSpeech': None,
    'time': None,
    'settingsLabels': [],
    'textLetters': []
}

