"""This class holds the settings of the game. For now they are hard-coded."""


class Settings:

    programName = 'Casual Word Game'

    programVersion = '1.2.0'

    # Indicates how many letters to reveal from a word (0.5 means half of the letters, 0.3 one third of the letters
    # etc.)
    revealLettersRatio = 0.5

    # Indicates the number of attempts to guess the word
    attempts = revealLettersRatio + 1

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
                'skip': f"{controlCharacter}skip"
                }

    @classmethod
    def initial_prompt(cls, **kwargs):
        print(f"\n{55 * '='}\n\n{cls.programName.upper()}\nv{cls.programVersion}\n\nReady to have " +
              "some fun? Ok, here we go.\nThe rules are very simple."
              f"\nTry to guess what the word by making a 'position-letter' " +
              "guess that consists of a position"
              "\n(the row of numbers below the word" +
              " marks the positions) and a letter that you think is at that position."
              "\n\nFor example: If you think that the letter 'i' is at position '4' in the word " +
              "type '4i' and hit 'ENTER'."
              "\nOr if you think you know the entire word just type it in and hit 'ENTER'." +
              f"\nRemember that you have a limited number of attempts." +
              "\n\nTo can get a 'part-of-speech' hint type in '>speech' to see it." +
              "\nIf you need a definition hint, type in '>define'." +
              "\nTo show synonyms of the word type in '>syn'."
              "\nTo let a random letter type in '>let'. Careful, this will also use up an attempt!"
              "\nTo skip this word and try anther one, type '>skip'."
              "\nTo quit the game at any time type '>exit'." +
              f"\nThat's it, have fun!"
              f"\n\nHere's the word spec:")
        for kw in kwargs:
            print(f"{str(kw).upper()}: {str(kwargs[kw])}")
        print("Can you guess what it is?\n")

    @classmethod
    def short_prompt(cls, **kwargs):
        print(f"\n\nHere's the new word:")
        for kw in kwargs:
            print(f"{str(kw).upper()}: {str(kwargs[kw])}")

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
