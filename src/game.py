"""Casual Word Game Class"""
import json
import re
import sys
from random import choice as choose
from settings import Settings


class Game:

    def __init__(self, words_file: object = None):
        """The game class initializer"""

        self.words_file_path = Settings.defaultWordsFile if words_file is None else str(words_file)
        self.wordDict = self.load_words(self.words_file_path)
        self.word = {}
        self.wordStructure = []
        self.wordIsActive = False
        self.prompt = True
        self.shortPrompt = False

    @staticmethod
    def load_words(words_file: str) -> dict:
        """Return a word dictionary

        :param words_file: A URL string of the word JSON file.
        """

        # If the word file could not be accessed...
        try:
            _words_file = open(words_file)
        # ...end the game
        except (OSError, FileNotFoundError):
            sys.exit("\n\nCouldn't load the game's word file. Check that it exists at the location specified " +
                     f"('{words_file}')"
                     "\nExiting program.\n")
        # ...Else...
        words_obj, _dict = json.loads(_words_file.read()), {}
        # ...construct a mini dictionary for each non-digit word that doesn't contain white space, dashes and has a
        # definition and synonym[s]
        for word in words_obj.keys():
            _word = str(word)
            keys = words_obj[_word].keys()
            if ' ' not in _word and '-' not in _word and not _word.isdigit() \
                    and 'definitions' in keys and len(words_obj[_word]['definitions']) != 0 \
                    and 'synonyms' in words_obj[_word]['definitions'][0].keys():
                _dict[_word.upper()] = {
                    'word': _word.upper(),
                    'partOfSpeech': str(words_obj[_word]['definitions'][0]['partOfSpeech']).capitalize(),
                    'def': str(words_obj[_word]['definitions'][0]['definition']).capitalize(),
                    'synonyms': list(words_obj[_word]['definitions'][0]['synonyms']).copy(),
                    'attempts': len(_word) // 2,
                    'showLetters': len(_word) // 2
                }
        _words_file.close()
        return _dict

    def choose_word(self) -> dict:
        """Choose a random word from the list

        :returns: A random word from the game's word list as a dictionary
        """

        chosen_word, self.wordIsActive = self.wordDict[choose(list(self.wordDict.keys()))], False
        return chosen_word

    def update_word_structure(self, letter: str = '', position: int = 0, silent: bool = True, prompt: bool = False,
                              short_prompt: bool = False, test_mode: bool = False) -> None:
        """Update the word structure

        :param letter: A letter to put in the word structure of the game
        :param position: An integer denoting the position in the word structure at which to put the letter
        :param silent: Controls weather to print the word (False) or not (True). Default is False
        :param prompt: Controls weather to display a prompt (False) or not (True). Default is False
        :param short_prompt: Controls weather to print a short prompt (False) or not (True). Default is False
        :param test_mode: Tells the method to run in 'test mode'. Test mode is used only for testing purposes
        """

        word_length = len(self.word['word'])

        # If a word structure initialization attempt is made...
        # ...(usually at the beginning of the game on an empty 'wordDict')...
        if letter == '' and position == 0:
            self.wordStructure[:], _letter = [], 0
            # Pick some random positions...
            positions, random_positions, i = list(range(word_length)), [], 0
            while i < self.word['showLetters']:
                _position = choose(positions)
                random_positions.append(_position)
                positions.remove(_position)
                i += 1
            # ...and build the word structure
            else:
                while _letter < len(self.word['word']):
                    if _letter in random_positions:
                        self.wordStructure.append(self.word['word'][_letter])
                    else:
                        self.wordStructure.append('_')
                    _letter += 1

        # Else - just update the word structure with a letter
        else:
            self.wordStructure[position] = letter.upper()

        # ...and finally print the word if desired
        if not silent and not test_mode:
            if not short_prompt:
                self.print_word(prompt)
            else:
                self.print_word(short_prompt=short_prompt)

    def print_word(self, prompt: bool = False, short_prompt: bool = False) -> None:
        """Print the word to the screen

        :param prompt: Controls weather to display a prompt. Default is False
        :param short_prompt: Controls weather to print a short prompt. Default is False
        """

        masked_word, positions, position = '', '', 0
        for letter in self.wordStructure:
            masked_word += f"{str(letter + ' ').center(4)}"
            position += 1
            positions += f"{str(' ' + str(position)).center(4)}"
        # If a prompt is supplied (usually at the beginning of the game) then display it
        if prompt:
            print(f"\n{55 * '='}\n\n{Settings.programName.upper()}\nv{Settings.programVersion}\n\nReady to have " +
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
                  "\nTo skip this word and try anther one, type '>skip'."
                  "\nTo quit the game at any time type '>exit'." +
                  f"\nThat's it, have fun!"
                  f"\n\nHere's the word spec:"
                  f"\nLETTERS: {len(self.word['word'])}" +
                  f"\nDEFINITION: '{self.word['def']}'" +
                  f"\nATTEMPTS: {self.word['attempts']}" +
                  "\nCan you guess what it is?\n")
        # If a 'short prompt' is supplied (usually when continuing the game after a successful guess or skipping a word)
        elif short_prompt:
            print(f"\n\nHere's the new word:"
                  f"\nLETTERS: {len(self.word['word'])}" +
                  f"\nDEFINITION: '{self.word['def']}'" +
                  f"\nATTEMPTS: {self.word['attempts']}\n")
        print('\n', masked_word, '\n')
        print(positions, '\n')

    def define(self) -> None:
        """Define a word"""

        print(f"\n'{self.word['def']}'\n")
        self.collect_guess()

    def speech(self) -> None:
        """Print a word's part of speech attribute"""

        print(f"\n'{self.word['partOfSpeech']}'\n")
        self.collect_guess()

    def syn(self) -> None:
        """Print a word's synonym[s]"""

        synonyms = ''
        for syn in self.word['synonyms']:
            synonyms += f"{str(syn).capitalize()}, "
        synonyms = synonyms.strip(', ')
        print(f"\n{synonyms}\n")
        self.collect_guess()

    def collect_guess(self, test_mode: bool = False) -> None:
        """Collect the guess

        :param test_mode: Tells the method to run in 'test mode'. Test mode is used only for testing purposes
        """

        if test_mode:
            return

        # This holds the guess
        guess = input().upper()

        if len(guess.strip()) == 0:
            self.collect_guess()

        # First determine the guess type:
        # Could be either a 'position - letter' or a 'whole word' type.
        # The 'position - letter' type fo guess let's the program check weather a particular guessed letter
        # is at a certain position in the word.
        # The 'whole word' type of guess let's the program check if the guessed word is indeed the word being guessed
        #
        # The type of guess is determined by the syntax of it after input into the console,
        # e.g.:
        # If the input contains a 'digit character' pattern the guess is considered to be a 'position-letter' one,
        # if it doesn't contain a digit pattern it is considered to be a 'whole word' one.

        # Before the guess processing check for some control flow keywords
        # If an attempt to exit the game is made - exit the game
        if guess == '>EXIT':
            self.stop()

        # If a word speech hint is requested - display it
        elif guess == '>SPEECH':
            self.speech()

        # If a word definition is requested - display one
        elif guess == '>DEFINE':
            self.define()

        # If a word synonyms are requested - display them
        elif guess == '>SYN':
            self.syn()

        # If another word is requested - restart the game
        elif guess == '>SKIP':
            self.shortPrompt = True
            self.start()

        # A Regular expression describing the 'position - letter' speech
        letter_position_guess_type = re.fullmatch(r'^(\d+)\s*(\w+)$', guess)

        # A Regular expression describing the 'whole word' speech
        whole_word_guess_type = True if not letter_position_guess_type else None

        # If the guess is of speech 'position - letter'...
        if letter_position_guess_type:
            self.process_letter_guess(letter_position_guess_type)

        # Or if the guess is of speech 'whole word'...
        elif whole_word_guess_type:
            self.process_whole_word_guess(guess)

        # Continue the 'guessing' game if the word is not complete...
        self.game_flow()

    def process_whole_word_guess(self, guess: re.Match) -> None:
        """Process a whole word guess

        :param string guess: The guess as typed into the standard input
        """

        # ...if the guess word is the same as the word to be guessed
        if guess.upper() == self.word['word'].upper():
            print(f"\n'{self.word['word']}' GREAT! YOU GUESSED THE WORD.")
            self.wordIsActive = True
        else:
            self.word['attempts'] -= 1
            if self.word['attempts'] == 0:
                print("\nGAME OVER. NO MORE ATTEMPTS REMAINING :(\n")
                self.wordIsActive = True
            else:
                print('\nSORRY WRONG GUESS. TRY AGAIN.\n' + f"{self.word['attempts']} try/ies remaining.\n")
                self.print_word()

    def process_letter_guess(self, letter_position_guess_type: re.Match) -> None:
        """Process a letter guess

        :param re.Match letter_position_guess_type: The match from the regex matching
        """

        guess_position, guess_letter = \
            int(letter_position_guess_type.groups()[0]) - 1, letter_position_guess_type.groups()[1].upper()
        # If the letter is already revealed...
        if self.wordStructure[guess_position] != '_':
            print('\nThis letter is already revealed. Try the another one.\n')
            self.print_word()
        # ...if the guess is correct (the guessed 'letter' is indeed at the specified 'position' in the word)
        # and has not been revealed before
        elif self.word['word'][guess_position] == guess_letter:
            # ...update the word structure
            self.update_word_structure(letter=guess_letter, position=guess_position, silent=True)
            # ...and if there are still letters to be guessed - continue with the game
            if '_' in self.wordStructure:
                print('\nWELL DONE! YOU GUESSED A LETTER RIGHT. KEEP GOING.\n')
                self.print_word()
            # ...or there are no more letters - consider the word guessed and the game - complete
            elif '_' not in self.wordStructure:
                print(f"\n'{self.word['word']}' GREAT! YOU GUESSED THE WORD.")
                self.wordIsActive = True

        # ...if the guess is not correct
        else:
            self.word['attempts'] -= 1
            if self.word['attempts'] == 0:
                print("\nGAME OVER. SORRY, NO MORE ATTEMPTS REMAINING :(\n")
                self.wordIsActive = True
            else:
                print('\nSORRY WRONG GUESS. TRY AGAIN.\n' + f"{self.word['attempts']} attempt[s] remaining.\n")
                self.print_word()

    def game_flow(self) -> None:
        """The game flow"""

        # If the word is still in play...
        if not self.wordIsActive:
            # ...continue the game
            self.collect_guess()
        # ... or if not...
        else:
            # ...offer to continue the game with a different word or exit the game
            self.exit_prompt()

    def exit_prompt(self) -> None:
        """Prompt for action at game end"""

        choice = input("\n\nWhat do you want to do next:\nType '>continue' to continue " +
                       "playing with a different word\nOr type '>exit' to exit " +
                       "the game?").upper()
        # If a choice to continue playing is made
        if choice == '>CONTINUE':
            # ...continue with the game
            self.prompt = False
            self.shortPrompt = True
            self.start()
        # ...else exit the game
        elif choice == '>EXIT':
            self.stop()
        # ...else if no game flow key word is recognized, re-prompt
        else:
            self.exit_prompt()

    def start(self, test_mode: bool = False) -> None:
        """Start the game

        :param bool test_mode: Tells the method to run in 'test mode'. Test mode is used only for testing purposes
        """

        # Choose a word from the list first
        self.word = self.choose_word()

        # then update the word structure
        self.update_word_structure(prompt=self.prompt, short_prompt=self.shortPrompt,
                                   silent=False, test_mode=test_mode)

        # ...and collect the guess
        if not test_mode:
            try:
                self.collect_guess(test_mode)
            except KeyboardInterrupt:
                pass

    def stop(self) -> None:
        """Stop the game"""

        sys.exit()
