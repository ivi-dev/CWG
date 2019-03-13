import json
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from os.path import join, split
from random import choice
from threading import Timer
from typing import Tuple

from playsound import playsound

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

        # General items
        self.mainWindow = self.winfo_toplevel()
        self.mainCanvas = self.thinLineImg = None
        self.wordStructure = []
        self.wordIsActive = False
        self.timerActive = True
        self.timer = None
        self.markedLetter = None

        # Settings related items
        self.settingsWindow = None
        self.settingsMainCanvas = None
        self.activeSetting = None
        self.activeOptions = []
        self.activeOptionsWindow = None

        self.init_settings()
        self.load_words(join(split(sys.argv[0])[0], 'data', 'words.json') if words_file is None
                        else str(words_file))
        self.build_main_ui()

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

    def configure_window(self, window: tk.Toplevel, title: str = settings.programName + ' ' + settings.programVersion,
                         min_size: Tuple[int, int] = (style.mainWindowMinWidth, style.mainWindowMinHeight),
                         max_size: Tuple[int, int] = (style.mainWindowMinWidth, style.mainWindowMinHeight),
                         **bindings) -> tk.Toplevel:
        """Setup the main window and frame for drawing the UI

        :param window: The window to configure
        :param title: The title of the window
        :param min_size: The minimum size of the window
        :param max_size: The maximum size of the window
        :param bindings: A key-value pairs of the event types and handlers to bind to the window
        """
        
        # Setup the main/root window
        window.title(title)
        window.minsize(min_size[0], min_size[1])
        window.maxsize(max_size[0], max_size[1])
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        for eventType in bindings:
            self.mainWindow.bind('<' + str(eventType) + '>', bindings[eventType])
        else:
            self.sticky_frame(self)
            return window

    def sticky_frame(self, frame: tk.Widget) -> tk.Widget:
        """Make a frame resizable

        :param frame: The frame to configure
        """
        # Make the main frame fluid/extensible
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.grid(sticky=tk.W + tk.E + tk.N + tk.S)
        return frame

    def init_settings(self, settings_file: str = settings.settingsFile):
        """Initialize the settings with the data from the settings file"""
        settings_ = {}
        with open(settings_file, 'r') as file:
            settings_ = json.loads(file.read())
        if settings_ == {}:
            raise IOError('Could not update the settings. Make sure that the settings file is where it\'s '
                          'supposed to be and is in the correct JSON syntax.')
        else:
            for key in settings_.keys():
                setattr(settings, key, settings_[key])

    def build_main_ui(self):
        """Build the main game's UI"""
        # Configure the main window/canvas
        self.configure_window(self.mainWindow, KeyPress=self.__guess_letter, Destroy=self.__exit_game)

        self.mainCanvas = tk.Canvas(self, bg=style.mainBGColor, highlightthickness=0, relief='ridge')
        self.mainCanvas.grid(sticky=tk.W + tk.E + tk.N + tk.S)

        # Place the background image
        self.mainCanvas.create_image(170, 250, image=Game.register_image(PhotoImage(Image.open(
            os.path.abspath('src/data/images/speech_bubble_550x369.png')))))

        # Place the logo image
        logo_img = self.mainCanvas.create_image(40, 40, image=Game.register_image(PhotoImage(Image.open(
                                             os.path.abspath('src/data/images/logo_50x50.png')))))

        # The word definition
        content.canvasElements['wordDef'] = self.mainCanvas.create_text(80, 20, text=content.word['def'],
                                                                        fill=style.white,
                                                                        font=(style.mainFont[0], 16),
                                                                        width=style.mainWindowMinWidth -
                                                                        self.mainCanvas.bbox(logo_img)[2] * 2,
                                                                        anchor=tk.NW)

        # The letters
        self.place_letters()

        # THE INFO AREA
        # The thin line
        thin_line_img = Game.register_image(PhotoImage(Image.open(os.path.abspath('src/data/images/line.png'))))

        # Place the thick line
        self.mainCanvas.create_image(2, 240, image=Game.register_image(PhotoImage(Image.open(
                                    os.path.abspath('src/data/images/thick_line.png')))),
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
                                                      os.path.abspath('src/data/images/clock_low_shadow.png')))),
                                             anchor=tk.N+tk.W)

        # The time remaining
        content.canvasElements['time'] = self.mainCanvas.create_text(self.mainCanvas.coords(clock)[0] + 65,
                                    self.mainCanvas.coords(clock)[1] + 78, text=Game.sec_to_min(content.word['time']),
                                    fill=style.fadedWhite, font=(style.mainFont[0], 23))

        # The buttons
        button_images = [Game.register_image(PhotoImage(Image.open(
            os.path.abspath('src/data/images/' + button + '_button.png')))) for button
                         in content.buttonLabels]
        buttons, bindings, i = [], [self.__skip_word, self.__letter_hint, self.__settings, self.__exit_game], 0
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

    def build_settings_ui(self):
        """Construct the settings window's UI"""
        # Main frame
        settings_main_frame = ttk.Frame(self.settingsWindow)
        self.sticky_frame(settings_main_frame)

        # Main canvas
        settings_main_canvas = tk.Canvas(settings_main_frame, bg=style.mainBGColor, highlightthickness=0,
                                         relief='ridge')
        settings_main_canvas.grid(sticky=tk.W + tk.E + tk.N + tk.S)
        self.settingsMainCanvas = settings_main_canvas

        # The background image
        settings_main_canvas.create_image(style.mainWindowMinWidth - style.mainWindowMinWidth // 5,
                                          style.mainWindowMinHeight // 5,
                                          image=Game.register_image(PhotoImage(Image.open(
                                            os.path.abspath('src/data/images/cog_wheel.png')))))

        # The settings items
        thin_line_img = Game.register_image(PhotoImage(Image.open(os.path.abspath('src/data/images/line.png'))))

        labels, lines, i = [], [], 0
        for label in content.settingsLabels:
            if i != 0:
                style.settingsLabelY += 50
            content.canvasElements['settingsLabels'].append((settings_main_canvas.create_text(0, style.settingsLabelY,
                                                             text=label[0] + ': ' +
                                                             str(getattr(settings, label[-1])).capitalize(),
                                                             fill=style.white,
                                                             font=style.mainFont, anchor=tk.W),
                                                             label[2], label[0]))
            labels.append(content.canvasElements['settingsLabels'][i][0])
            settings_main_canvas.tag_bind(content.canvasElements['settingsLabels'][i][0], '<1>', self.__show_options)
            lines.append(settings_main_canvas.create_image(0, style.settingsLabelY + 25, image=thin_line_img,
                                                           anchor=tk.W))
            i += 1
        else:
            # Center the labels
            style.settingsLabelY = 50
            for label in labels:
                label_bbox = settings_main_canvas.bbox(label)
                label_width = label_bbox[2] - label_bbox[0]
                settings_main_canvas.move(label, (style.mainWindowMinWidth - label_width) // 2, 0)
            else:
                for line in lines:
                    line_bbox = settings_main_canvas.bbox(line)
                    line_width = line_bbox[2] - line_bbox[0]
                    settings_main_canvas.move(line, (style.mainWindowMinWidth - line_width) // 2, 0)
                else:
                    first_label_bbox = settings_main_canvas.bbox(labels[0])
                    last_label_bbox = settings_main_canvas.bbox(labels[-1])
                    first_line_bbox = settings_main_canvas.bbox(lines[0])
                    last_line_bbox = settings_main_canvas.bbox(lines[-1])

                    settings_block_height = last_line_bbox[2] - first_label_bbox[0]
                    for item in (labels + lines):
                        settings_main_canvas.move(item, 0, (style.mainWindowMinHeight - settings_block_height) // 10)

        # The buttons
        button_images = [Game.register_image(PhotoImage(Image.open(
            os.path.abspath('src/data/images/' + button + '_button.png')))) for button
            in content.settingsButtonLabels]
        buttons, bindings, i = [], [self.__apply_settings, self.__cancel_settings], 0
        for buttonImg in button_images:
            if i != 0:
                x = 0
                for index in range(i):
                    x += button_images[index].width() + 20
                style.buttonX = x + 60
            buttons.append(settings_main_canvas.create_image(style.buttonX, 425, image=buttonImg, anchor=tk.N + tk.W))
            settings_main_canvas.tag_bind(buttons[i], '<1>', bindings[i])
            i += 1
        else:
            # Center the buttons
            style.buttonX = 60
            last_button_x = settings_main_canvas.coords(buttons[-1])[1]
            for button in buttons:
                settings_main_canvas.move(button, (style.mainWindowMinWidth - (last_button_x + button_images[-1].width())) + 40, 0)

    def __show_options(self, event: tk.Event):
        """Show the options for a setting item

        :param event: The tk event object
        """
        # Get the location of the mouse click
        click_location_x = event.x
        click_location_y = event.y
        # Get the text value of the option label that was clicked
        clicked_label = None
        for label in content.canvasElements['settingsLabels']:
            label_bbox = self.settingsMainCanvas.bbox(label[0])
            if label_bbox[0] < click_location_x < label_bbox[2] and label_bbox[1] < click_location_y < label_bbox[3]:
                clicked_label = label
                break
        self.activeSetting = clicked_label[0]  # The settings that is being reviewed
        clicked_label_bbox = self.settingsMainCanvas.bbox(clicked_label[0])
        # Show the option window and remove any visible ones
        self.clear_options_windows()
        option_window = self.settingsMainCanvas.create_rectangle(clicked_label_bbox[0], clicked_label_bbox[1] +
                                                 (clicked_label_bbox[3] - clicked_label_bbox[1]), clicked_label_bbox[2],
                                                 clicked_label_bbox[3] +
                                                 (clicked_label_bbox[3] - clicked_label_bbox[1]) + 25,
                                                 fill=style.darkGrey, outline=style.grey, width=4)
        self.activeOptionsWindow = option_window  # The currently open options box
        # List the options inside of the window
        option_window_bbox = self.settingsMainCanvas.bbox(option_window)
        options = getattr(settings, clicked_label[1] + 'Options')
        fill = style.white
        selected_option = str(self.settingsMainCanvas.itemcget(clicked_label[0], 'text')).split(':')[1].strip()
        x, i, options_ = option_window_bbox[0] + 15, 0, []
        for option in options:
            if i != 0:
                previous_option_bbox = self.settingsMainCanvas.bbox(options_[i - 1])
                x += previous_option_bbox[2] - previous_option_bbox[0] + 20
            fill = style.white if option == selected_option else style.grey
            options_.append(self.settingsMainCanvas.create_text(x, option_window_bbox[1] + 15,
                                                                text=option, font=(style.mainFont[0], 18),
                                                                fill=fill, anchor=tk.NW))
            self.activeOptions = options_
            self.settingsMainCanvas.tag_bind(options_[i], '<1>', self.__select_option)
            i += 1
        else:
            # Center the options inside the options window
            last_option_x = self.settingsMainCanvas.bbox(options_[-1])[2]
            x_move = (option_window_bbox[2] - last_option_x) // 2 - 10
            for option in options_:
                self.settingsMainCanvas.move(option, x_move, 0)

    def clear_options_windows(self):
        """Removes an option widow and the options inside"""
        for option_ in self.activeOptions:
            self.settingsMainCanvas.delete(option_)
        self.settingsMainCanvas.delete(self.activeOptionsWindow)

    def __select_option(self, event: tk.Event):
        """Handles a selection of an option

        :param event: The tk event object
        """
        click_point = (event.x, event.y)
        for option in self.activeOptions:
            option_bbox = self.settingsMainCanvas.bbox(option)
            if option_bbox[0] < click_point[0] < option_bbox[2] and option_bbox[1] < click_point[1] < option_bbox[3]:
                option_text = self.settingsMainCanvas.itemcget(option, 'text')
                active_setting_label = str(self.settingsMainCanvas.itemcget(self.activeSetting, 'text')).split(':')[0]
                self.settingsMainCanvas.itemconfigure(self.activeSetting, text=active_setting_label + ': ' +
                                                      option_text)
                # Set the corresponding option to the selected value
                for option__ in content.canvasElements['settingsLabels']:
                    if option__[2] == active_setting_label:
                        setattr(settings, option__[1], option_text)
                # Remove the options window
                self.clear_options_windows()
                break

    def __apply_settings(self, event: tk.Event):
        """Apply settings

        :param event: The tk event
        """
        self.write_settings()
        self.close_window(self.settingsWindow, 'settingsWindow')

    def __cancel_settings(self, event: tk.Event):
        """Cancel put of the settings

        :param event: The tk event
        """
        self.close_window(self.settingsWindow, 'settingsWindow')

    def write_settings(self, settings_file: str = settings.settingsFile):
        """Write settings to a file"""
        # First collect the current state of the settings
        settings_ = {}
        for setting in content.canvasElements['settingsLabels']:
            settings_[setting[1]] = str(getattr(settings, setting[1]))
        else:  # and then write them to a file
            file_id = None
            with open(settings_file, 'w') as settings_file:
                file_id = settings_file.write(json.dumps(settings_, sort_keys=True, indent=4))
            if file_id is None:
                raise IOError('Could not update the settings. Make sure that the settings file is where it\'s '
                              'supposed to be and is in the correct JSON syntax.')

    def close_window(self, window: tk.Toplevel, window_ref: str = ''):
        """Close a gui window

        :param window: The tk.TopLevel object to close
        :param window_ref: A name of a variable holding a reference to the window.
         If this value is not an empty string the reference will be cleared
        """
        window.destroy()
        if window_ref != '':
            setattr(self, window_ref, None)

    def place_letters(self):
        """Place a word's letters on screen"""

        # Remove the letter objects and refs
        if 'letters' in content.canvasElements.keys():
            for letter in content.canvasElements['letters']:
                self.mainCanvas.delete(letter)
            else:
                del content.canvasElements['letters']

        letters, i, word_length = [], 0, len(content.word['word'])
        style.letterWidth = style.letterHeight = (style.mainWindowMinWidth // word_length) - 20 if \
            (style.mainWindowMinWidth // word_length) - 20 <= 120 else 120
        while i < word_length:
            style.letterX = (10 * (i + 1)) if i == 0 else (10 * (i + 1)) + style.letterWidth * i
            letters.append(self.mainCanvas.create_rectangle(style.letterX,
                                                            style.letterY, style.letterX +
                                                            style.letterWidth,
                                                            style.letterY + style.letterHeight,
                                                            fill=style.hiddenLetterBG,
                                                            outline=style.hiddenLetterBG))
            self.mainCanvas.tag_bind(letters[i], '<1>', self.__mark_letter)
            i += 1
        else:
            # Center the letters
            style.letterX = 10
            last_letter_x = self.mainCanvas.coords(letters[-1])[2]
            for letter in letters:
                self.mainCanvas.move(letter, (style.mainWindowMinWidth - last_letter_x) / 2 - style.letterX, 0)
            content.canvasElements['letters'] = letters

    def count_letters(self, letters: str) -> int:
        """Count the hidden/revealed letters

        :param letters: The type of letters to count, either 'hidden' or 'revealed'
        """
        hidden, revealed = [], []
        for letter in content.canvasElements['letters']:
            fill = self.mainCanvas.itemcget(letter, 'fill')
            if fill == style.hiddenLetterBG:
                hidden.append(letter)
            elif fill == style.guessedLetterBG:
                revealed.append(letter)
        else:
            print(len(hidden), len(revealed))
            if letters == 'revealed':
                return len(revealed)
            return len(hidden)

    def __guess_letter(self, event: tk.Event):
        """Process a typed letter and see if its guessed position matches the real one

        :param event: The event as passed by the tkinter binding
        """
        if self.markedLetter is not None and content.word['attempts'] != 0:
            letter, i, letter__ = str(event.char).upper(), 0, None
            for letter_ in content.canvasElements['letters']:
                letter__ = letter_
                if letter_ == self.markedLetter:
                    break
                i += 1
            if content.word['word'][i] == letter:  # If the letters match...
                self.reveal_letter(letter__, letter)
                self.signal_correct_guess()
                if self.is_word_guessed():  # If all letters are guessed correctly
                    self.stop_clock()
                    self.signal_word_guessed()
                    self.auto_load_word()
            else:
                self.signal_incorrect_guess()
                # Decrement the attempts
                content.word['attempts'] -= 1
                self.update_attempts(content.word['attempts'])
            if content.word['attempts'] == 0:  # If no more attempts are left...
                self.stop_clock()
                self.signal_game_over()

    def auto_load_word(self):
        """Load a random word"""
        self.after(1000, self.__skip_word)

    def is_word_guessed(self) -> bool:
        """Check weather the word is guessed"""
        word = ''
        for letter in content.canvasElements['letters']:
            if self.mainCanvas.itemcget(letter, 'fill') == style.guessedLetterBG:
                guessed_letter_coordinates = self.mainCanvas.coords(letter)
                letter_ = self.mainCanvas.find_overlapping(guessed_letter_coordinates[0], guessed_letter_coordinates[1],
                                                           guessed_letter_coordinates[2],
                                                           guessed_letter_coordinates[3])[-1]
                letter__ = self.mainCanvas.itemcget(letter_, 'text')
                word += letter__
        else:
            if word == content.word['word']:
                return True
            else:
                return False

    def signal_word_guessed(self, sound: str = 'src/data/sound/word_correct.wav'):
        """Signal with sound the correct guess of a word

        :param sound: The path to the sound file. Default is src/data/sound/word_correct.wav
        """
        playsound(sound, False)

    def signal_correct_guess(self, sound: str = 'src/data/sound/correct.wav'):
        """Signal with sound that a letter was guessed correctly

        :param sound: The path to the sound file. Default is src/data/sound/correct.wav
        """
        playsound(sound, False)

    def signal_hint(self, sound: str = 'src/data/sound/hint.wav'):
        """Signal with sound a hinted letter

        :param sound: The path to the sound file. Default is src/data/sound/hint.wav
        """
        playsound(sound, False)


    def signal_incorrect_guess(self, sound: str = 'src/data/sound/incorrect.wav'):
        """Signal with sound the a letter was guessed incorrectly

        :param sound: The path to the sound file. Default is src/data/sound/incorrect.wav
        """
        playsound(sound, False)

    def signal_game_over(self, sound: str = 'src/data/sound/game_over.wav'):
        """Signal game over. That happens when the attempts are exhausted or the time ran out

        :param sound: The path to the sound file. Default is src/data/sound/game_over.wav
        """
        playsound(sound, False)
        content.word['attempts'] = 0
        self.update_attempts(0)
        self.markedLetter = None
        self.reset_letters()

    def reset_letters(self, letters: list = None) -> bool:
        """Unmark letters of the word

        :param letters: A list of canvas ids fo letters to reset (return to normal background color)
        """
        if letters is not None:
            for letter in letters:
                self.mainCanvas.itemconfigure(letter, fill=style.hiddenLetterBG)
            else:
                return True
        else:
            for letter in content.canvasElements['letters']:
                self.mainCanvas.itemconfigure(letter, fill=style.hiddenLetterBG)
            else:
                return True

    def update_attempts(self, attempts: int):
        """Update the displayed attempts

        :param attempts: The current number of attempts
        """
        self.mainCanvas.itemconfigure(content.canvasElements['attempts'],
                                      text=str(self.mainCanvas.itemcget(content.canvasElements['attempts'], 'text'))
                                      .split()[0] + ' ' + str(attempts))

    def reveal_letter(self, letter_id: int, word_letter: str) -> tuple:
        """Reveal a letter on the canvas

        :param letter_id: The canvas id of the letter to reveal
        :param word_letter: The letter from a word that's being guessed
        :returns: A 2-tuple with the canvas letter id and the revealed letter
        """
        self.mainCanvas.itemconfigure(letter_id, fill=style.guessedLetterBG)
        letter_box = self.mainCanvas.bbox(letter_id)
        letter_box_width = letter_box_height = letter_box[2] - letter_box[0]
        content.canvasElements['textLetters'].append(self.mainCanvas.create_text(letter_box[0] + letter_box_width // 2,
                                                     letter_box[1] + letter_box_height // 2,
                                                     text=word_letter, font=(style.mainFont[0],
                                                                             -round(letter_box_width * 0.75)),
                                                     fill=style.white))
        self.markedLetter = None
        return letter_id, word_letter

    def __mark_letter(self, event: tk.Event):
        """Marks a letter as active, meaning that any key press is going to be interpreted
        as an attempt to guess that letter

        :param event: The event as passed by the tkinter binding
        """
        click_coordinates = (event.x, event.y)
        for letter in content.canvasElements['letters']:
            letter_box = self.mainCanvas.bbox(letter)
            letter_top_left_x = letter_box[0]
            letter_top_left_y = letter_box[1]
            letter_bottom_right_x = letter_box[2]
            letter_bottom_right_y = letter_box[3]
            if letter_top_left_x < click_coordinates[0] < letter_bottom_right_x and \
                    letter_top_left_y < click_coordinates[1] < letter_bottom_right_y:
                if self.mainCanvas.itemcget(letter, 'fill') == style.guessedLetterBG:
                    break
                if self.mainCanvas.itemcget(letter, 'fill') == style.hiddenLetterBG:
                    self.mainCanvas.itemconfigure(letter, fill=style.markedLetterBG)
                    for letter_ in content.canvasElements['letters']:  # Reset the others
                        if letter_ != letter and self.mainCanvas.itemcget(letter_, 'fill') != style.guessedLetterBG:
                            self.mainCanvas.itemconfigure(letter_, fill=style.hiddenLetterBG)
                    self.markedLetter = letter
                else:
                    self.mainCanvas.itemconfigure(letter, fill=style.hiddenLetterBG)
                    self.markedLetter = None
                break

    def load_words(self, words_file: str) -> dict:
        """Load a list of words from a JSON file

        :param words_file: A URL string of the words JSON file
        :returns: The loaded words database
        """

        _words_file, words_obj, _dict = None, dict, {}
        try:
            _words_file = open(words_file)
        except (OSError, FileNotFoundError):
            raise Exception('The game\'s words database is not accessible for some reason. Terminating.')
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
                    'word': _word.upper(),
                    'partOfSpeech': str(words_obj[_word]['definitions'][0]['partOfSpeech']).capitalize(),
                    'def': str(words_obj[_word]['definitions'][0]['definition']).capitalize() + '.',
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
        chosen_word['attempts'] = (round(len(chosen_word['word']) * settings.attemptsRatio[settings.difficulty]))
        chosen_word['time'] = settings.time[settings.difficulty]
        content.word = chosen_word
        # self.update_word_structure()
        return chosen_word

    # def update_word_structure(self, letter: str = None, position: int = None) -> list:
    #     """Update the word structure. The word structure is list that keeps track what state a word's letters are in,
    #     either 'hidden' or 'revealed'
    #
    #     :param letter: A letter to put in the word structure
    #     :param position: An integer denoting the position in the word structure at which to put the letter
    #     :returns: The updated word structure
    #     """
    #     word_length = len(content.word['word'])
    #     # If a word structure initialization attempt is made...
    #     # ...(usually at the beginning of the game on an empty 'wordDict')...
    #     if letter is None and position is None:
    #         self.wordStructure[:], _letter = [], 0
    #         # Pick some random positions...
    #         positions, random_positions, i = list(range(word_length)), [], 0
    #         while i < round(word_length * settings.revealLettersRatio[settings.difficulty]):
    #             _position = choice(positions)
    #             random_positions.append(_position)
    #             positions.remove(_position)
    #             i += 1
    #         # ...and build the word structure
    #         else:
    #             while _letter < word_length:
    #                 if _letter in random_positions:
    #                     self.wordStructure.append(content.word['word'][_letter])
    #                 else:
    #                     self.wordStructure.append('_')
    #                 _letter += 1
    #
    #     # Else - just update the word structure with a letter
    #     elif letter is not None and position is not None:
    #         self.wordStructure[position] = letter.upper()
    #     else:
    #         raise Exception('You have to either specify both \'letter\' and \'position\' '
    #                         'arguments or leave them both None')
    #     return self.wordStructure

    @staticmethod
    def sec_to_min(seconds: int) -> str:
        """Convert seconds to minutes

        :param seconds: A number of seconds
        :returns: The minutes+seconds representation of a number of seconds
        """
        if seconds == 0:
            raise ZeroDivisionError()
        seconds_ = abs(seconds)
        initial_calc = str(round(seconds_ / 60, 2))
        minutes, seconds_fraction, seconds = initial_calc.split('.')[0], initial_calc.split('.')[1], 0
        seconds = str(seconds_ - (int(minutes) * 60))
        # if seconds_fraction != '0':
        #     seconds = float('0.' + seconds_fraction) * 60
        # else:
        #     seconds = '00'
        seconds_final = seconds if seconds != '0' else '00'
        return minutes + ':' + seconds_final

    def count_down(self):
        """Decrement the remaining time"""
        if self.timerActive:
            current_time: str = self.mainCanvas.itemcget(content.canvasElements['time'], 'text')
            current_time_split = current_time.split(':')
            current_minutes, current_seconds = int(current_time_split[0]), int(current_time_split[1])
            if current_seconds == 0 and current_minutes != 0:
                current_minutes -= 1
                current_seconds = 59
            elif current_seconds == 0 and current_minutes == 0:
                self.signal_game_over()
                return
            else:
                current_seconds -= 1
            current_seconds_corrected = str(current_seconds) if current_seconds >= 10 else '0' + str(current_seconds)
            self.mainCanvas.itemconfigure(content.canvasElements['time'],
                                          text=str(current_minutes) + ':' + current_seconds_corrected)
            self.timer = Timer(1.0, self.count_down)
            self.timer.start()

    @staticmethod
    def pretty_list(list_: list,
                    enclose_char: str = "'",
                    sep_char: str = ', ',
                    text_transform: str = 'capitalize') -> str:
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

    def __skip_word(self, event: tk.Event = None) -> dict:
        """Skip a word (choose a new word and resume the game)

        :param event: The event object passed in by the binding
        :returns: The newly chosen word
        """
        chosen_word = self.choose_word()
        self.refresh_ui()
        self.restart_clock()
        return chosen_word

    def reset_clock(self):
        """Reset the time"""
        self.mainCanvas.itemconfigure(content.canvasElements['time'],
                                      text=Game.sec_to_min(settings.time[settings.difficulty]))

    def restart_clock(self):
        """Restart the timer"""
        if self.timer is not None:
            self.timer.cancel()
        self.reset_clock()
        self.timerActive = True
        self.count_down()

    def stop_clock(self):
        """Stop the time"""
        if self.timer is not None:
            self.timer.cancel()
        self.timer = None
        self.timerActive = False

    def __letter_hint(self, event: tk.Event) -> str:
        """Reveal an extra letter

        :param event: the tk Event object
        :returns: The revealed letter
        """
        # Only if half or more letters are still hidden
        if self.count_letters('revealed') < len(content.word['word']) // 3:
            hidden, i = [], 0
            for letter in content.canvasElements['letters']:
                if self.mainCanvas.itemcget(letter, 'fill') == style.hiddenLetterBG or \
                        self.mainCanvas.itemcget(letter, 'fill') == style.markedLetterBG:
                    hidden.append((letter, i))
                i += 1
            else:
                random_letter = choice(hidden)
                self.reveal_letter(random_letter[0], content.word['word'][random_letter[1]])
                self.signal_hint()
                content.word['attempts'] -= 1
                self.update_attempts(content.word['attempts'])
                return content.word['word'][random_letter[1]]

    def __settings(self, event: tk.Event):
        """Go to the settings screen"""
        # If a settings windows is not open
        if self.settingsWindow is None:
            self.settingsWindow = tk.Toplevel(width=200, height=100, takefocus=True)
            self.settingsWindow.lift()
            self.configure_window(self.settingsWindow, 'Settings')
            self.build_settings_ui()
        else:  # Else, move the focus to the already open settings window
            self.settingsWindow.focus_set()

    def __exit_game(self, event: tk.Event):
        """Stop and exit the game

        :param event: The event object passed by the binding
        """
        try:
            self.stop_clock()
            self.quit()
        except KeyboardInterrupt:
            pass

    def refresh_ui(self):
        """Refresh the UI, normally when a new word is chosen"""

        # Update the word definition
        self.mainCanvas.itemconfigure(content.canvasElements['wordDef'], text=content.word['def'])

        # Update the letters/remove the text letters
        self.place_letters()
        for letter in content.canvasElements['textLetters']:
            self.mainCanvas.delete(letter)

        # Update the attempts
        self.update_attempts(content.word['attempts'])

        # Update the synonyms
        self.mainCanvas.itemconfigure(content.canvasElements['synonyms'],
                                      text=str(self.mainCanvas.itemcget(content.canvasElements['synonyms'], 'text'))
                                      .split()[0] + ' ' + Game.pretty_list(content.word['synonyms']))

        # Update the part of speech
        self.mainCanvas.itemconfigure(content.canvasElements['partOfSpeech'],
                                      text=Game.pretty_list(str(
                                          self.mainCanvas.itemcget(content.canvasElements['partOfSpeech'], 'text'))
                                      .split()[:3], '', ' ', 'upper') + ' ' + str(content.word['partOfSpeech']))

    def start(self):
        """Start the game"""
        self.count_down()
        self.mainloop()

