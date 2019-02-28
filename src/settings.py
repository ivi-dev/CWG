"""This class holds the settings of the game. For now they are hard-coded."""


class Settings:

    programName = 'Casual Word Game'

    programVersion = '1.2.1'

    # Controls the game's difficulty. Could be either 'easy', 'medium' (the default) or 'hard'
    difficulty = 'medium'

    # Indicates how many letters to reveal from a word (0.5 means half of the letters, 0.3 one third of the letters
    # etc.). Varies with the 'difficulty'
    revealLettersRatio = {'easy': 0.5,
                          'medium': 0.5,
                          'hard': 0.3}

    # Indicates the number of attempts to guess the word. The numbers mean 'add that many to the value of
    # revealLettersRatio'. Example: On the 'easy' setting if there are 3 letters revealed, one would have 5 (3 + 2)
    # attempts to guess the word. Varies with the 'difficulty'
    attempts = {'easy': 2,
                'medium': 1,
                'hard': 0}

    # Game flow character. It tells the program that a word following this character calls for an action other than a
    # guess e.g: typing <controlCharacter>EXIT is not trying to guess the word 'EXIT' but trying to quit/exit the game
    controlCharacter = '>'

    # Keywords. Those follow the 'controlCharacter' to construct a command
    keywords = {'exit': f"{controlCharacter}exit",
                'speech': f"{controlCharacter}speech",
                'def': f"{controlCharacter}def",
                'syn': f"{controlCharacter}syn",
                'let': f"{controlCharacter}let",
                'att': f"{controlCharacter}att",
                'skip': f"{controlCharacter}skip",
                'diff': f"{controlCharacter}diff"
                }

    @classmethod
    def get_type(cls, attribute: any) -> str:
        """Return the type of a setting attribute

        :param attribute: The setting attribute to check
        """

        return str(type(attribute)).replace('<class ', '').replace('>', '')

    @classmethod
    def change(cls, setting: str, value: any) -> any:
        """Change the value of a setting

        :param setting: The name of the setting to change
        :param value: The value to set
        """

        # If the 'setting' does nor exist in the settings pool...
        setting_value: any
        try:
            setting_value = getattr(cls, setting)
        except AttributeError:
            # ...raise an exception and quit the operation
            raise

        # ...Else if the value types don't match...
        if type(setting_value) != type(value):
            # ...quit the operation
            raise TypeError(f"The '{setting}' is of type " +
                            f"{cls.get_type(setting_value)}" +
                            f" you provided {cls.get_type(value)}.")

        # ...Else if all ok change the value
        setattr(cls, setting, value)
        return value
