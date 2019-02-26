"""This class holds the settings of the game. For now they are hard-coded."""


class Settings:

    programName = 'Casual Word Game'

    programVersion = '1.1.0'

    # Indicates how many letters to reveal from a word (0.5 means half of the letters, 0.3 one third of the letters
    # etc.)
    revealLettersRatio = 0.5

    # Indicates the number of attempts to guess the word
    attempts = revealLettersRatio + 1
