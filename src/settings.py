import os


class Settings:

    # The default location of the 'words' file. This file serves as the primary pool of words to use for the game
    defaultWordsFile = os.path.abspath('src/data/words.json')

    def __init__(self):
        pass
