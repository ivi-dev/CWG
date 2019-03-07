import os
import tkinter as tk
import tkinter.ttk as ttk
import gui_settings as settings
from PIL import Image
from PIL.ImageTk import PhotoImage
from style import style
from content import content


class Game(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.mainWindow = self.winfo_toplevel()
        self.mainCanvas = self.thinLineImg = None
        self.infoLabels = []

        self.build_ui()

    @staticmethod
    def register_image(img: PhotoImage) -> PhotoImage:
        """Stores a ref to an image so that it gets displayed properly
        :param img: The image to store a ref for
        :returns: The image that was stored
        """
        content['images'].append(img)
        if img not in content['images']:
            raise IndexError('The image Id \'' + str(img) + '\' was not added to the image storage ' +
                             'for some reason. As a consequence the image denoted by that Id might not be ' +
                             'visible on the UI.')
        else:
            return img

    def configure_app(self):
        """Setup the canvas for drawing the UI"""
        
        # Setup the main/root window
        self.mainWindow.title(settings.programName + ' ' + settings.programVersion)
        self.mainWindow.minsize(style['mainWindowMinWidth'], style['mainWindowMinHeight'])
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

        self.mainCanvas = tk.Canvas(self, bg=style['mainBGColor'], highlightthickness=0, relief='ridge')
        self.mainCanvas.grid(sticky=tk.W + tk.E + tk.N + tk.S)

        # Place the background image

        self.mainCanvas.create_image(170, 250, image=Game.register_image(PhotoImage(Image.open(
            os.path.abspath('src/data/speech_bubble_550x369.png')))))

        # Place the logo image
        self.mainCanvas.create_image(40, 40, image=Game.register_image(PhotoImage(Image.open(
                                             os.path.abspath('src/data/logo_50x50.png')))))

        # The word definition
        self.mainCanvas.create_text(80, 40, text='One of the four seasons', 
                                    fill=style['white'],
                                    font=style['mainFont'], anchor=tk.W)

        # The word's letters
        letters = []
        for i in range(4):
            style['letterX'] = (10 * (i + 1)) if i == 0 else (10 * (i + 1)) + style['letterWidth'] * i
            letters.append(self.mainCanvas.create_rectangle(style['letterX'],
                                                            style['letterY'], style['letterX'] +
                                                            style['letterWidth'],
                                                            style['letterY'] + style['letterHeight'],
                                                            fill=style['hiddenLetterBG'],
                                                            outline=style['hiddenLetterBG']))
        else:
            # Center the letters
            style['letterX'] = 10
            last_letter_x = self.mainCanvas.coords(letters[-1])[2]
            for letter in letters:
                self.mainCanvas.move(letter, 
                                     (style['mainWindowMinWidth'] - last_letter_x) / 2 - style['letterX'], 0)

        # THE INFO AREA
        # The thin line
        thin_line_img = Game.register_image(PhotoImage(Image.open(os.path.abspath('src/data/line.png'))))

        # Place the thick line
        self.mainCanvas.create_image(2, 240, image=Game.register_image(PhotoImage(Image.open(
                                    os.path.abspath('src/data/thick_line.png')))),
                                    anchor=tk.W)

        # The info labels
        info_labels_elements = []
        # Place the info labels
        i = 0
        for label in content['infoLabels']:
            if i != 0:
                style['infoLabelY'] += 50
            info_labels_elements.append(self.mainCanvas.create_text(20, style['infoLabelY'], 
                                                                    text=label[0] + ': ' + label[1],
                                                                    fill=style['white'],
                                                                    font=style['mainFont'], anchor=tk.W))
            self.mainCanvas.create_image(0, style['infoLabelY'] + 25, image=thin_line_img, anchor=tk.W)
            i += 1
        else:
            style['infoLabelY'] = 270

        # The clock
        clock = self.mainCanvas.create_image(thin_line_img.width() + 60, style['infoLabelY'], 
                                             image=Game.register_image(PhotoImage(Image.open(
                                                      os.path.abspath('src/data/clock_low_shadow.png')))),
                                             anchor=tk.N+tk.W)

        # The time remaining
        self.mainCanvas.create_text(self.mainCanvas.coords(clock)[0] + 43,
                                    self.mainCanvas.coords(clock)[1] + 78, text='21',
                                    fill=style['fadedWhite'], font=(style['mainFont'][0], 40), anchor=tk.W)

        # The buttons
        button_images = [Game.register_image(PhotoImage(Image.open(
            os.path.abspath('src/data/' + button + '_button.png')))) for button
                         in content['buttonLabels']]
        buttons, i = [], 0
        for buttonImg in button_images:
            if i != 0:
                x = 0
                for index in range(i):
                    x += button_images[index].width() + 20
                style['buttonX'] = x + 60
            buttons.append(self.mainCanvas.create_image(style['buttonX'], 425, image=buttonImg, anchor=tk.N+tk.W))
            i += 1
        else:
            # Center the buttons
            style['buttonX'] = 60
            last_button_x = self.mainCanvas.coords(buttons[-1])[1]
            for button in buttons:
                self.mainCanvas.move(button, (style['mainWindowMinWidth'] - (last_button_x + button_images[-1].width()))
                                     / 2 - style['buttonX'] / 2, 0)

    def start(self):
        """Start the game"""
        self.mainloop()

