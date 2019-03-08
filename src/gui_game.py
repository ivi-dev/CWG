import json
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from os.path import join, split
from random import choice

import gui_settings as settings
from PIL import Image
from PIL.ImageTk import PhotoImage
import style
import content


class Game(ttk.Frame):
    def __init__(self, words_file: object = None):
        """Constructor

        :param words_file: The path to the words file
        """
        super().__init__()

        self.mainWindow = self.winfo_toplevel()
        self.mainCanvas = self.thinLineImg = None

        # Initialize the words database
        self.load_words(join(split(sys.argv[0])[0], 'data', 'words.json') if words_file is None
                        else str(words_file))

        self.wordIsActive = False

        self.build_ui()

    @staticmethod
    def register_image(img: PhotoImage) -> PhotoImage:
        """Stores a ref to an image so that it gets displayed properly

        :param img: The image to store a ref for
        :returns: The image that was stored
        """
        content.images.append(img)
        if img not in content.images:
            raise IndexError('The image Id \'' + str(img) + '\' was not added to the image storage ' +
                             'for some reason. As a consequence the image denoted by that Id might not be ' +
                             'visible on the UI.')
        else:
            return img

    def configure_app(self):
        """Setup the canvas for drawing the UI"""
        
        # Setup the main/root window
        self.mainWindow.title(settings.programName + ' ' + settings.programVersion)
        self.mainWindow.minsize(style.mainWindowMinWidth, style.mainWindowMinHeight)
        self.mainWindow.maxsize(650, 450)
        self.mainWindow.rowconfigure(0, weight=1)
        self.mainWindow.columnconfigure(0, weight=1)

        # Make the main frame fluid/extensible
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky=tk.W + tk.E + tk.N + tk.S)

    def build_ui(self):
        """Build the UI"""

        # First, configure the canvas
        self.configure_app()

        self.mainCanvas = tk.Canvas(self, bg=style.mainBGColor, highlightthickness=0, relief='ridge')
        self.mainCanvas.grid(sticky=tk.W + tk.E + tk.N + tk.S)

        # Place the background image
        self.mainCanvas.create_image(170, 250, image=Game.register_image(PhotoImage(Image.open(
            os.path.abspath('src/data/speech_bubble_550x369.png')))))

        # Place the logo image
        logo_img = self.mainCanvas.create_image(40, 40, image=Game.register_image(PhotoImage(Image.open(
                                             os.path.abspath('src/data/logo_50x50.png')))))

        # The word definition
        content.canvasElements['wordDef'] = self.mainCanvas.create_text(80, 20, text=content.word['def'],
                                                                        fill=style.white,
                                                                        font=style.mainFont,
                                                                        width=style.mainWindowMinWidth -
                                                                        self.mainCanvas.bbox(logo_img)[2] * 2,
                                                                        anchor=tk.NW)

        # The letters
        self.place_letters()

        # THE INFO AREA
        # The thin line
        thin_line_img = Game.register_image(PhotoImage(Image.open(os.path.abspath('src/data/line.png'))))

        # Place the thick line
        self.mainCanvas.create_image(2, 240, image=Game.register_image(PhotoImage(Image.open(
                                    os.path.abspath('src/data/thick_line.png')))),
                                    anchor=tk.W)

        # The info labels
        i = 0
        for label in content.infoLabels:
            if i != 0:
                style.infoLabelY += 50
            content.canvasElements[label[1]] = self.mainCanvas.create_text(20, style.infoLabelY, text=label[0] + ': ' +
                                                                            (Game.pretty_list(content.word[label[1]])
                                                                             if Game.get_type(content.word[label[1]]) ==
                                                                                'list'
                                                                             else str(content.word[label[1]])),
                                                                           fill=style.white,
                                                                           font=style.mainFont, anchor=tk.W)
            self.mainCanvas.create_image(0, style.infoLabelY + 25, image=thin_line_img, anchor=tk.W)
            i += 1
        else:
            style.infoLabelY = 270

        # The clock
        clock = self.mainCanvas.create_image(thin_line_img.width() + 80, style.infoLabelY,
                                             image=Game.register_image(PhotoImage(Image.open(
                                                      os.path.abspath('src/data/clock_low_shadow.png')))),
                                             anchor=tk.N+tk.W)

        # The time remaining
        self.mainCanvas.create_text(self.mainCanvas.coords(clock)[0] + 43,
                                    self.mainCanvas.coords(clock)[1] + 78, text='21',
                                    fill=style.fadedWhite, font=(style.mainFont[0], 40), anchor=tk.W)

        # The buttons
        button_images = [Game.register_image(PhotoImage(Image.open(
            os.path.abspath('src/data/' + button + '_button.png')))) for button
                         in content.buttonLabels]
        buttons, bindings, i = [], [self.__skip_word, self.__reveal_letter, self.__settings, self.__exit_game], 0
        for buttonImg in button_images:
            if i != 0:
                x = 0
                for index in range(i):
                    x += button_images[index].width() + 20
                style.buttonX = x + 60
            buttons.append(self.mainCanvas.create_image(style.buttonX, 425, image=buttonImg, anchor=tk.N+tk.W))
            self.mainCanvas.tag_bind(buttons[i], '<1>', bindings[i])
            i += 1
        else:
            # Center the buttons
            style.buttonX = 60
            last_button_x = self.mainCanvas.coords(buttons[-1])[1]
            for button in buttons:
                self.mainCanvas.move(button, (style.mainWindowMinWidth - (last_button_x + button_images[-1].width()))
                                     / 2 - style.buttonX / 2, 0)

    def place_letters(self):
        """Place a word's letters on screen"""

        # Remove the letter objects and refs
        if 'letters' in content.canvasElements.keys():
            for letter in content.canvasElements['letters']:
                self.mainCanvas.delete(letter)
            else:
                del content.canvasElements['letters']

        letters, i, word_length = [], 0, len(content.word['word'])
        style.letterWidth = style.letterHeight = (style.mainWindowMinWidth // word_length) - 20
        while i < word_length:
            style.letterX = (10 * (i + 1)) if i == 0 else (10 * (i + 1)) + style.letterWidth * i
            letters.append(self.mainCanvas.create_rectangle(style.letterX,
                                                            style.letterY, style.letterX +
                                                            style.letterWidth,
                                                            style.letterY + style.letterHeight,
                                                            fill=style.hiddenLetterBG,
                                                            outline=style.hiddenLetterBG))
            i += 1
        else:
            # Center the letters
            style.letterX = 10
            last_letter_x = self.mainCanvas.coords(letters[-1])[2]
            for letter in letters:
                self.mainCanvas.move(letter,
                                     (style.mainWindowMinWidth - last_letter_x) / 2 - style.letterX, 0)
            content.canvasElements['letters'] = letters

    def load_words(self, words_file: str) -> dict:
        """Load a list of words from a JSON file

        :param words_file: A URL string of the words JSON file
        :returns: The loaded words database
        """

        _words_file, words_obj, _dict = None, dict, {}
        try:
            _words_file = open(words_file)
        except (OSError, FileNotFoundError):
            # TODO: Decide what to do if the words file is not accessible
            raise
        finally:
            if _words_file is not None:
                words_obj = json.loads(_words_file.read())
                _words_file.close()

        for word in words_obj.keys():
            _word = str(word)
            keys = words_obj[_word].keys()
            if ' ' not in _word and '-' not in _word and not _word.isdigit() \
                    and 'definitions' in keys and len(words_obj[_word]['definitions']) != 0 \
                    and 'synonyms' in words_obj[_word]['definitions'][0].keys():
                _dict[_word.upper()] = {
                    'word': _word.upper() + '.',
                    'partOfSpeech': str(words_obj[_word]['definitions'][0]['partOfSpeech']).capitalize(),
                    'def': str(words_obj[_word]['definitions'][0]['definition']).capitalize(),
                    'synonyms': list(words_obj[_word]['definitions'][0]['synonyms']).copy()
                }
        content.wordsDB = _dict
        self.choose_word()
        return content.wordsDB

    def choose_word(self) -> dict:
        """Choose a random word from the words database

        :returns: A random word from the game's words database
        """

        chosen_word, self.wordIsActive = content.wordsDB[choice(list(content.wordsDB.keys()))], False
        chosen_word['showLetters'] = round(len(chosen_word['word']) * settings.revealLettersRatio[settings.difficulty])
        chosen_word['attempts'] = (round(len(chosen_word['word']) * settings.revealLettersRatio[settings.difficulty])) \
            + settings.attempts[settings.difficulty]
        content.word = chosen_word
        return chosen_word

    @staticmethod
    def pretty_list(list_: list, enclose_char: str = "'", sep_char: str = ', ', text_transform: str = 'capitalize') -> str:
        """Return a clean string view of a list

        :param list_: A non-empty list of items
        :param enclose_char: A character to enclose each item of the list with. Default is ('')
        :param sep_char: A character to separate each item of the list. Default is (blank space)
        :param text_transform: The transformation to apply to each item of the list.
        Could be either 'capitalize' (Default), 'lower' or 'upper'
        :returns: A string in which all of the items in a 'list' are enclosed by a 'enclose_char'
         and are separated by a 'sep_char' character
        """
        if len(list_) == 0:
            raise ValueError('The list you provided is empty.')
        else:
            pretty_str = ''
            for item in list_:
                item_ = str(item).capitalize()
                if text_transform.lower() == 'lower':
                    item_ = str(item).lower()
                elif text_transform.lower() == 'upper':
                    item_ = str(item).upper()
                pretty_str += enclose_char + item_ + enclose_char + sep_char
            else:
                return pretty_str.rstrip(sep_char)

    @classmethod
    def get_type(cls, attribute: any) -> str:
        """Return the type of an attribute

        :param attribute: The attribute to check
        :returns: The newly chosen word
        """
        return str(type(attribute)).replace('<class ', '').replace('>', '').replace('\'', '')

    def __skip_word(self, event: tk.Event) -> dict:
        """Skip a word (choose a new word and resume the game)

        :param event: The event object passed in by the binding
        :returns: The newly chosen word
        """
        chosen_word = self.choose_word()
        self.refresh_ui()
        return chosen_word

    def __reveal_letter(self) -> str:
        """Reveal an extra letter

        :returns: The revealed letter
        """
        pass

    def __settings(self) -> bool:
        """Go to the settings screen

        :returns: True on successful navigation, False on failure
        """
        pass

    def __exit_game(self) -> bool:
        """Stop and exit the game

        :returns: True on successful navigation, False on failure
        """
        pass

    def refresh_ui(self):
        """Refresh the UI, normally when a new word is chosen"""

        # Update the word definition
        self.mainCanvas.itemconfigure(content.canvasElements['wordDef'], text=content.word['def'])

        # Update the letters
        self.place_letters()

        # Update the attempts
        self.mainCanvas.itemconfigure(content.canvasElements['attempts'],
                                      text=str(self.mainCanvas.itemcget(content.canvasElements['attempts'], 'text'))
                                      .split()[0] + ' ' + str(content.word['attempts']))

        # Update the synonyms
        self.mainCanvas.itemconfigure(content.canvasElements['synonyms'],
                                      text=str(self.mainCanvas.itemcget(content.canvasElements['synonyms'], 'text'))
                                      .split()[0] + ' ' + Game.pretty_list(content.word['synonyms']))

        # Update the part of speech
        self.mainCanvas.itemconfigure(content.canvasElements['partOfSpeech'],
                                      text=Game.pretty_list(str(self.mainCanvas.itemcget(content.canvasElements['partOfSpeech'], 'text'))
                                      .split()[:3], '', ' ', 'upper') + ' ' + str(content.word['partOfSpeech']))
        # TODO: Find out why there's a little comma-like character in the output on screen

        # Update the time
        self.mainCanvas.itemconfigure(content.canvasElements['wordDef'], text=content.word['def'])

    def start(self):
        """Start the game"""

        self.mainloop()

