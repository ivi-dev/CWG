import unittest
import re
from src.game import Game
from unittest.mock import Mock


class TestGame(unittest.TestCase):

    game: Game
    mock_game: Mock

    @classmethod
    def setUpClass(cls):
        try:
            cls.game = Game('../../src/data/words.json')
            cls.mock_game = Mock(Game)
        except TypeError:
            TestGame.tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        del cls.game

    def test_game_initialized(self):
        self.assertIsInstance(self.game, Game, 'A test game is not and instance of the "Game" class.')
        self.assertIsInstance(self.game.wordDict, dict, 'The word dictionary of the game is not of type "dict".')
        self.assertIsNot(len(self.game.wordDict.keys()), 0, 'The word dictionary is empty at the beginning of ' +
                         'the game.')
        self.assertIsInstance(self.game.word, dict, 'The game\'s word is not of type "dict" before the start of ' +
                              'the game.')
        self.assertIsInstance(self.game.wordStructure, list, 'The games word structure is not of type "dict" ' +
                              'before the start of the game.')

    def test_game_start(self):
        TestGame.mock_game.start(test_mode=True)
        TestGame.mock_game.start.assert_called_with(test_mode=True)

        self.game.start(test_mode=True)
        self.assertNotEqual(self.game.word.keys(), 0, 'The word is empty after the start of the game.')
        self.assertNotEqual(len(self.game.wordStructure), 0, 'The word structure is empty after the start of the game.')

    def test_load_words(self):
        words: dict = self.game.load_words(self.game.words_file_path)
        self.assertIsInstance(words, dict, "The word returned from the 'load_words' method is not a 'dict'.")
        self.assertNotEqual(words.keys(), 0, "The dictionary returned from the 'load_words' method is empty.")

    def test_choose_word(self):
        word: dict = self.game.choose_word()
        self.assertIsInstance(word, dict, "The word returned from the 'choose_word' method is not a 'dict'.")
        self.assertNotEqual(word.keys(), 0, "The dictionary returned from the 'choose_word' method is empty.")
        self.assertIn(word['word'], self.game.wordDict, "The returned from the 'choose_word' method " +
                      "is not in the word dictionary.")

    def test_collect_guess(self):
        TestGame.mock_game.collect_guess(test_mode=True)
        TestGame.mock_game.collect_guess.assert_called_with(test_mode=True)

    def test_print_word(self):
        TestGame.mock_game.print_word(prompt=True, short_prompt=True)
        TestGame.mock_game.print_word.assert_called_with(prompt=True, short_prompt=True)

    def test_process_letter_guess(self):
        match = re.match(r"a", "a")
        TestGame.mock_game.process_letter_guess(match)
        TestGame.mock_game.process_letter_guess.assert_called_with(match)

    def test_process_whole_word_guess(self):
        match = re.match(r"a", "a")
        TestGame.mock_game.process_whole_word_guess(match)
        TestGame.mock_game.process_whole_word_guess.assert_called_with(match)


if __name__ == '__main__':
    unittest.main()
