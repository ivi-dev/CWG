from settings import Settings


class Prompts:

    @classmethod
    def initial_prompt(cls, **kwargs) -> None:
        """This is the long explanatory text, usually shown at the beginning of the game"""

        print(f"\n{55 * '='}\n\n{Settings.programName.upper()}\nv{Settings.programVersion}\n\nReady to have "
              "some fun? Ok, here we go.\nThe rules are very simple."
              f"\nTry to guess what the word by making a 'position-letter' "
              "guess that consists of a position"
              "\n(the row of numbers below the word"
              " marks the positions) and a letter that you think is at that position."
              "\n\nFor example: If you think that the letter 'i' is at position '4' in the word "
              "type '4i' and hit 'ENTER'."
              "\nOr if you think you know the entire word just type it in and hit 'ENTER'."
              f"\nRemember that you have a limited number of attempts."
              "\n\nTo can get a 'part-of-speech' hint type in '>speech' to see it."
              "\nIf you need a definition hint, type in '>define'."
              "\nTo show synonyms of the word type in '>syn'."
              "\nTo let a random letter type in '>let'. Careful, this will also use up an attempt!"
              "\nTo skip this word and try anther one, type '>skip'."
              "\nTo change the difficulty of the game, type '>diff easy|medium|hard'"
              " or just '>diff' without arguments to see the current setting."
              "\nTo quit the game at any time type '>exit'."
              f"\nThat's it, have fun!"
              f"\n\nHere's the word spec:")
        for kw in kwargs:
            print(f"{str(kw).upper()}: {str(kwargs[kw])}")
        print("Can you guess what it is?\n")

    @classmethod
    def short_prompt(cls, **kwargs) -> None:
        """This is the short text, usually shown when switching words"""

        print(f"\n\nHere's the new word:")
        for kw in kwargs:
            print(f"{str(kw).upper()}: {str(kwargs[kw])}")
