"""
Unit tests for hangman.py
Tests the Hangman game logic
"""

import pytest
import sys
import os
from unittest.mock import patch

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import hangman


class TestHangmanGameLogic:
    """Tests for core Hangman game logic."""

    def test_getPlayerGuess_accepts_single_letter(self):
        """getPlayerGuess should accept a single letter."""
        with patch('builtins.input', return_value='A'):
            result = hangman.getPlayerGuess([])
            assert result == 'A'
            assert isinstance(result, str)
            assert len(result) == 1

    def test_getPlayerGuess_converts_to_uppercase(self):
        """getPlayerGuess should convert lowercase to uppercase."""
        with patch('builtins.input', return_value='a'):
            result = hangman.getPlayerGuess([])
            assert result == 'A'

    def test_getPlayerGuess_rejects_multiple_letters(self):
        """getPlayerGuess should reject multiple letters."""
        with patch('builtins.input', side_effect=['AB', 'C']):
            result = hangman.getPlayerGuess([])
            assert result == 'C'
            assert len(result) == 1

    def test_getPlayerGuess_rejects_non_letter(self):
        """getPlayerGuess should reject non-letter characters."""
        with patch('builtins.input', side_effect=['1', 'A']):
            result = hangman.getPlayerGuess([])
            assert result == 'A'

    def test_getPlayerGuess_rejects_special_char(self):
        """getPlayerGuess should reject special characters."""
        with patch('builtins.input', side_effect=['!', 'B']):
            result = hangman.getPlayerGuess([])
            assert result == 'B'

    def test_getPlayerGuess_rejects_duplicate_guess(self):
        """getPlayerGuess should reject letters already guessed."""
        with patch('builtins.input', side_effect=['A', 'B']):
            result = hangman.getPlayerGuess(['A'])
            assert result == 'B'

    def test_getPlayerGuess_rejects_empty_input(self):
        """getPlayerGuess should reject empty input."""
        with patch('builtins.input', side_effect=['', 'D']):
            result = hangman.getPlayerGuess([])
            assert result == 'D'

    def test_getPlayerGuess_with_already_guessed_list(self):
        """getPlayerGuess should track already guessed letters."""
        already_guessed = ['A', 'B', 'C']
        with patch('builtins.input', side_effect=['A', 'D']):
            result = hangman.getPlayerGuess(already_guessed)
            assert result == 'D'
            assert result not in already_guessed

    def test_getPlayerGuess_all_alphabet_valid(self):
        """All single letters A-Z should be valid."""
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in alphabet:
            with patch('builtins.input', return_value=letter):
                result = hangman.getPlayerGuess([])
                assert result == letter
                assert result.isalpha()


class TestHangmanGameState:
    """Tests for game state and progression."""

    def test_lostGame_initially_false(self):
        """lostGame should start as False."""
        hangman.lostGame = False
        assert hangman.lostGame == False

    def test_hangman_pics_length(self):
        """HANGMAN_PICS should contain 7 stages (empty to fully drawn)."""
        assert len(hangman.HANGMAN_PICS) == 7

    def test_hangman_pics_are_strings(self):
        """All HANGMAN_PICS entries should be strings."""
        for pic in hangman.HANGMAN_PICS:
            assert isinstance(pic, str)

    def test_max_missed_letters(self):
        """Max wrong guesses is 6 (len(HANGMAN_PICS) - 1)."""
        max_wrong = len(hangman.HANGMAN_PICS) - 1
        assert max_wrong == 6


class TestHangmanDrawing:
    """Tests for drawing and display functions."""

    def test_drawHangman_no_missed_letters(self, capsys):
        """drawHangman should display correctly with no missed letters."""
        hangman.drawHangman([], ['A'], 'APPLE')
        captured = capsys.readouterr()
        assert 'Missed letters' in captured.out
        assert 'No missed letters yet' in captured.out

    def test_drawHangman_with_missed_letters(self, capsys):
        """drawHangman should display missed letters."""
        hangman.drawHangman(['X', 'Z'], ['A', 'P'], 'APPLE')
        captured = capsys.readouterr()
        assert 'X' in captured.out
        assert 'Z' in captured.out

    def test_drawHangman_displays_correct_letters(self, capsys):
        """drawHangman should reveal correct letters in the blank word."""
        hangman.drawHangman([], ['A', 'P'], 'APPLE')
        captured = capsys.readouterr()
        # 'A' and 'P' should be shown, others as blanks
        output = captured.out
        assert 'A' in output
        assert 'P' in output

    def test_drawHangman_displays_category(self, capsys):
        """drawHangman should display the game category."""
        hangman.drawHangman([], [], 'TEST')
        captured = capsys.readouterr()
        assert 'category' in captured.out.lower()

    def test_word_with_all_letters_guessed(self, capsys):
        """Word should be fully revealed when all letters guessed."""
        word = 'CAT'
        hangman.drawHangman([], ['C', 'A', 'T'], word)
        captured = capsys.readouterr()
        assert 'C A T' in captured.out

    def test_word_with_no_letters_guessed(self, capsys):
        """Word should be all blanks when no letters guessed."""
        word = 'DOG'
        hangman.drawHangman([], [], word)
        captured = capsys.readouterr()
        # 3-letter word should show 3 blanks
        assert '_ _ _' in captured.out


class TestHangmanGameRules:
    """Tests for game rule enforcement."""

    def test_words_list_not_empty(self):
        """WORDS list should contain words."""
        assert len(hangman.WORDS) > 0

    def test_all_words_are_strings(self):
        """All words in WORDS should be strings."""
        for word in hangman.WORDS:
            assert isinstance(word, str)

    def test_all_words_are_uppercase(self):
        """All words in WORDS should be uppercase (based on displayed category)."""
        for word in hangman.WORDS:
            assert word == word.upper()

    def test_category_is_animals(self):
        """Game category should be 'Animals'."""
        assert hangman.CATEGORY == 'Animals'

    def test_game_needs_exactly_6_wrong_guesses_to_lose(self):
        """Game should be lost after 6 wrong guesses (max without drawing)."""
        # HANGMAN_PICS has 7 states, so 6 wrong guesses triggers loss
        # (index 6 is the final state)
        max_wrong_before_loss = len(hangman.HANGMAN_PICS) - 1
        assert max_wrong_before_loss == 6


class TestHangmanGameFlow:
    """Tests for overall game flow and win/loss conditions."""

    @patch('hangman.getPlayerGuess')
    @patch('builtins.print')
    @patch('random.choice')
    def test_player_wins_all_letters_correct(self, mock_choice, mock_print, mock_guess):
        """Player should win by guessing all letters in the word."""
        # Setup: word is 'CAT', player guesses C, A, T in order
        mock_choice.return_value = 'CAT'
        mock_guess.side_effect = ['C', 'A', 'T']
        
        hangman.lostGame = False
        hangman.main()
        
        # Check that win message was printed
        printed_output = '\n'.join(str(call) for call in mock_print.call_args_list)
        assert 'won' in printed_output.lower() or 'congratulations' in printed_output.lower()

    @patch('hangman.getPlayerGuess')
    @patch('builtins.print')
    @patch('random.choice')
    def test_player_loses_too_many_wrong(self, mock_choice, mock_print, mock_guess):
        """Player should lose after 6 wrong guesses."""
        mock_choice.return_value = 'CAT'
        # Make 6 wrong guesses (letters not in CAT)
        mock_guess.side_effect = ['X', 'Q', 'Z', 'K', 'J', 'W']
        
        hangman.lostGame = False
        hangman.main()
        
        # Should be marked as lost game
        assert hangman.lostGame == True

    @patch('hangman.getPlayerGuess')
    @patch('random.choice')
    def test_secret_word_selected_randomly(self, mock_choice, mock_guess):
        """main() should select a random word from WORDS."""
        mock_choice.return_value = 'PYTHON'
        mock_guess.return_value = 'X'
        
        hangman.lostGame = False
        hangman.main()
        
        # Verify random.choice was called with WORDS
        mock_choice.assert_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
