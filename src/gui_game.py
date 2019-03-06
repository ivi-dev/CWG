import os
import tkinter as tk
import tkinter.ttk as ttk
import gui_settings as settings
from PIL import Image
from PIL.ImageTk import PhotoImage

class Game(ttk.Frame):

    def __init__(self):

        # TODO: Move these to a separate module/class
        self.mainBGColor = '#3F4041'
        self.hiddenLetterBG = '#9F5343'
        self.mainFont = ('Chalkduster', 20)
        self.WHITE = '#fff'
        self.LIGHT_GREY = '#999897'

        self.mainWindowMinWidth = 650

        self.letterWidth = self.letterHeight = 120
        self.letterX = 10
        self.letterY = 100
        self.letters = []

        self.infoLabelY = 270



        # --------------------------------------------
        # Style definition
        # self.style = ttk.Style()
        # self.style.configure('Chalk.TLabel', font=self.mainFont, foreground=self.WHITE)
        # self.style.configure('.', background=self.mainBGColor)

        # --------------------------------------
        # The root widget
        super().__init__()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.rowconfigure(2, weight=1)

        self.grid(sticky=tk.W+tk.E+tk.N+tk.S)

        # The root/main window
        self.mainWindow = self.winfo_toplevel()
        self.mainWindow.title(settings.programName + ' ' + settings.programVersion)
        self.mainWindow.minsize(650, 450)
        self.mainWindow.rowconfigure(0, weight=1)
        self.mainWindow.columnconfigure(0, weight=1)

        # self.mainWindow.bind('<Configure>', self.__resize_text)
        # self.mainWindow.bind('<Visibility>', self.__resize_letters)



        # --------------------------------------
        # TODO: Decide on which strcture to use
        # ALTERNATIVE STRUCTURE
        self.mainCanvas = tk.Canvas(self, bg=self.mainBGColor, highlightthickness=0, relief='ridge')
        self.mainCanvas.grid(sticky=tk.W+tk.E+tk.N+tk.S)

        # The logo image
        self.logoImg = PhotoImage(Image.open(os.path.abspath('src/data/logo_50x50.png')))

        # A background image
        self.bgImg = PhotoImage(Image.open(os.path.abspath('src/data/speech_bubble_550x369.png')))

        # Place the background image
        self.bgImg_ = self.mainCanvas.create_image(320, 250, image=self.bgImg)

        # Place the logo image
        self.logo = self.mainCanvas.create_image(40, 40, image=self.logoImg)

        # The word definition
        self.wordDefinition = self.mainCanvas.create_text(80, 40, text='One of the four seasons', fill=self.WHITE,
                                                          font=self.mainFont, anchor=tk.W)

        # The word's letters
        for i in range(4):
            self.letterX = (10 * (i + 1)) if i == 0 else (10 * (i + 1)) + self.letterWidth * i
            self.letters.append(self.mainCanvas.create_rectangle(self.letterX,
                                                                 self.letterY, self.letterX + self.letterWidth,
                                                                 self.letterY + self.letterHeight,
                                                                 fill=self.hiddenLetterBG, outline=self.hiddenLetterBG))
        else:
            self.letterX = 10
            last_letter_x = self.mainCanvas.coords(self.letters[-1])[2]
            # Center the letters
            for letter in self.letters:
                self.mainCanvas.move(letter, (self.mainWindowMinWidth - last_letter_x) / 2 - self.letterX, 0)

        # THE INFO AREA
        # The thick line
        self.thickLineImg = PhotoImage(Image.open(os.path.abspath('src/data/thick_line.png')))

        # Place the thick line
        self.thickLineImg_ = self.mainCanvas.create_image(325, 240, image=self.thickLineImg)

        # The info labels
        self.infoLabelsRaw = [('ATTEMPTS', '3'),
                              ('SYNONYMS', '\'Autumn\', \'Harvest\''),
                              ('PART OF SPEECH', 'NOUN')]
        self.infoLabels = []
        # Place the info labels
        i = 0
        for label in self.infoLabelsRaw:
            if i != 0:
                self.infoLabelY += 20
            self.infoLabels.append(self.mainCanvas.create_text(50, self.infoLabelY, text=label[0], fill=self.WHITE,
                                   font=self.mainFont, anchor=tk.W))
            i += 1
        # # --------------------------------------
        # TODO: Decide on which strcture to use
        # # The top row (with the word definition)
        # self.wordDefinitionRow = ttk.Frame(self)
        # self.wordDefinitionRow.grid(sticky=tk.W+tk.E+tk.N)
        #
        # # The logo image
        # self.logoImg = tk.PhotoImage(file=os.path.abspath('src/data/logo_50x50.png'))
        # self.logoImg.configure(width=55, height=55)
        #
        # # The logo image canvas
        # self.logo = tk.Canvas(self.wordDefinitionRow, width=60, height=58, highlightthickness=0,
        #                       relief='ridge')
        # self.logo.create_image(30, 30, image=self.logoImg)
        # self.logo.grid()
        #
        # # The word definition text
        # self.wordDefinition = ttk.Label(self.wordDefinitionRow, text='One of the four seasons.', style='Chalk.TLabel')
        # self.wordDefinition.grid(row=0, column=1, padx=15)
        #
        # # --------------------------------------
        # # The letters row
        # self.lettersRow = ttk.Frame(self)
        # self.lettersRow.columnconfigure(0, weight=1)
        # self.lettersRow.columnconfigure(1, weight=1)
        # self.lettersRow.columnconfigure(2, weight=1)
        # self.lettersRow.columnconfigure(3, weight=1)
        # self.lettersRow.rowconfigure(0, weight=1)
        # self.lettersRow.grid(column=0, row=1, pady=20, sticky=tk.W+tk.E+tk.N+tk.S)
        #
        # # Letter #1
        # self.letter1 = tk.Canvas(self.lettersRow, width=self.letterWidth, height=self.letterWidth,
        #                          bg=self.hiddenLetterBG, highlightthickness=0, relief='ridge')
        # # self.logo.create_image(30, 30, image=self.logoImg)
        # self.letter1.grid(row=0, column=0, padx=3, sticky=tk.W+tk.E+tk.N+tk.S)
        #
        # # Letter #2
        # self.letter2 = tk.Canvas(self.lettersRow, width=self.letterWidth, height=self.letterWidth,
        #                          bg=self.hiddenLetterBG, highlightthickness=0, relief='ridge')
        # # self.logo.create_image(30, 30, image=self.logoImg)
        # self.letter2.grid(row=0, column=1, padx=3, sticky=tk.W+tk.E+tk.N+tk.S)
        #
        # # Letter #3
        # self.letter3 = tk.Canvas(self.lettersRow, width=self.letterWidth, height=self.letterWidth,
        #                          bg=self.hiddenLetterBG, highlightthickness=0, relief='ridge')
        # # self.logo.create_image(30, 30, image=self.logoImg)
        # self.letter3.grid(row=0, column=2, padx=3, sticky=tk.W+tk.E+tk.N+tk.S)
        #
        # # Letter #4
        # self.letter4 = tk.Canvas(self.lettersRow, width=self.letterWidth, height=self.letterWidth,
        #                          bg=self.hiddenLetterBG, highlightthickness=0, relief='ridge')
        # # self.logo.create_image(30, 30, image=self.logoImg)
        # self.letter4.grid(row=0, column=3, padx=3, sticky=tk.W+tk.E+tk.N+tk.S)
        #
        # # --------------------------------------
        # # The info row
        # self.infoRow = ttk.Frame(self)
        # self.infoRow.columnconfigure(0, weight=1)
        # self.infoRow.columnconfigure(1, weight=1)
        # self.infoRow.rowconfigure(0, weight=1)
        # self.infoRow.rowconfigure(1, weight=1)
        # self.infoRow.rowconfigure(2, weight=1)
        # self.infoRow.rowconfigure(3, weight=1)
        # self.infoRow.rowconfigure(4, weight=1)
        # self.infoRow.rowconfigure(5, weight=1)
        # self.infoRow.rowconfigure(6, weight=1)
        # self.infoRow.grid(row=2, sticky=tk.W+tk.E+tk.S+tk.N)
        #
        # # The thick line
        # # self.thickLineImg = tk.PhotoImage(file=os.path.abspath('src/data/thick_line.png'))
        # # self.thickLineImg.configure(width=520, height=10)
        #
        # self.thickLine = tk.Canvas(self.infoRow, height=5, bg=self.WHITE, highlightthickness=0, relief='ridge')
        # # self.thickLine.create_image(30, 30, image=self.thickLineImg)
        # self.thickLine.grid(columnspan=4, sticky=tk.W+tk.E)
        #
        # # The remaining attempts label
        # self.attemptsLabel = ttk.Label(self.infoRow, text='ATTEMPTS: 3', style='Chalk.TLabel')
        # self.attemptsLabel.grid(row=1, sticky=tk.W, pady=10, padx=10)
        #
        # # Thin line
        # self.thinLine1 = tk.Canvas(self.infoRow, bg=self.LIGHT_GREY, width=520, height=2, highlightthickness=0, relief='ridge')
        # self.thinLine1.grid(row=2, columnspan=3, sticky=tk.W+tk.E)
        #
        # # The synonyms label
        # self.synonymsLabel = ttk.Label(self.infoRow, text='SYNONYMS: \'Autumn\', \'Harvest\'', style='Chalk.TLabel')
        # self.synonymsLabel.grid(row=3, sticky=tk.W, pady=10, padx=10)
        #
        # # Thin line
        # self.thinLine2 = tk.Canvas(self.infoRow, bg=self.LIGHT_GREY, width=520, height=2, highlightthickness=0, relief='ridge')
        # self.thinLine2.grid(row=4, columnspan=3, sticky=tk.W+tk.E)
        #
        # # The part of speech label
        # self.partOfSpeechLabel = ttk.Label(self.infoRow, text='PART OF SPEECH: NOUN', style='Chalk.TLabel')
        # self.partOfSpeechLabel.grid(row=5, columnspan=3, sticky=tk.W, pady=10, padx=10)
        #
        # # Thin line
        # self.thinLine3 = tk.Canvas(self.infoRow, bg=self.LIGHT_GREY, width=520, height=2, highlightthickness=0, relief='ridge')
        # self.thinLine3.grid(row=6, columnspan=3, sticky=tk.W+tk.E)
        #
        # # Clock
        # self.clockImg = tk.PhotoImage(file=os.path.abspath('src/data/clock_100x121.png'))
        # self.clockImg.configure(width=200, height=230)
        #
        # self.clock = tk.Canvas(self.infoRow, width=150, height=150,
        #                        highlightthickness=0, relief='ridge', bg=self.mainBGColor)
        # self.clock.create_image(115, 130, image=self.clockImg)
        # self.clock.grid(row=1, column=3, rowspan=6, sticky=tk.E+tk.N+tk.W+tk.S)

    def __resize_text(self, event=None):
        """Change the size of text"""
        self.wordDefinition.configure(font=self.mainFont + ' ' + str(self.mainWindow.winfo_width() // 10))

    def __match_size(self, event):
        """Equal the sizes of two or more widgets"""


    def start(self):
        """Start the game"""
        self.mainloop()

