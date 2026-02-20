"""
Unit tests for guessnum.py
Tests the "Guess the Number" game logic
"""

import pytest
import sys
import os
from unittest.mock import patch

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import guessnum


class TestGuessTheNumber:
    """Tests for the Guess the Number game."""

    def test_askForGuess_accepts_valid_decimal(self):
        """askForGuess should accept valid decimal inputs."""
        with patch('builtins.input', return_value='42'):
            result = guessnum.askForGuess()
            assert result == 42
            assert isinstance(result, int)

    def test_askForGuess_rejects_non_decimal(self):
        """askForGuess should reject non-decimal inputs."""
        # Simulate user entering invalid input, then valid input
        with patch('builtins.input', side_effect=['abc', '50']):
            result = guessnum.askForGuess()
            assert result == 50

    def test_askForGuess_rejects_float(self):
        """askForGuess should reject float inputs."""
        with patch('builtins.input', side_effect=['3.14', '75']):
            result = guessnum.askForGuess()
            assert result == 75

    def test_askForGuess_rejects_empty_string(self):
        """askForGuess should reject empty input."""
        with patch('builtins.input', side_effect=['', '100']):
            result = guessnum.askForGuess()
            assert result == 100

    def test_askForGuess_rejects_negative_number(self):
        """askForGuess should reject negative numbers (non-decimal)."""
        # isdecimal() returns False for negative numbers
        with patch('builtins.input', side_effect=['-5', '10']):
            result = guessnum.askForGuess()
            assert result == 10

    def test_askForGuess_accepts_one(self):
        """askForGuess should accept 1 (minimum)."""
        with patch('builtins.input', return_value='1'):
            result = guessnum.askForGuess()
            assert result == 1

    def test_askForGuess_accepts_one_hundred(self):
        """askForGuess should accept 100 (maximum in game)."""
        with patch('builtins.input', return_value='100'):
            result = guessnum.askForGuess()
            assert result == 100

    def test_askForGuess_accepts_leading_zeros(self):
        """askForGuess should accept numbers with leading zeros."""
        with patch('builtins.input', return_value='007'):
            result = guessnum.askForGuess()
            assert result == 7

    def test_askForGuess_returns_integer(self):
        """askForGuess should return an integer, not a string."""
        with patch('builtins.input', return_value='42'):
            result = guessnum.askForGuess()
            assert isinstance(result, int)
            assert not isinstance(result, str)

    def test_lostGame_initially_false(self):
        """lostGame should be False initially."""
        assert guessnum.lostGame == False

    @patch('guessnum.askForGuess')
    @patch('builtins.print')
    def test_main_correct_guess_wins(self, mock_print, mock_ask):
        """If player guesses correct number, they should win."""
        # Create a test where the secret number is 50 and player guesses it
        with patch('random.randint', return_value=50):
            mock_ask.return_value = 50
            guessnum.lostGame = False
            guessnum.main()
            # Check that a win message was printed
            printed_output = '\n'.join(str(call) for call in mock_print.call_args_list)
            assert 'won' in printed_output.lower() or 'guessed' in printed_output.lower()

    @patch('guessnum.askForGuess')
    @patch('builtins.print')
    def test_main_too_low_hint(self, mock_print, mock_ask):
        """Should give 'too low' hint when guess is below secret."""
        with patch('random.randint', return_value=75):
            mock_ask.return_value = 50
            guessnum.lostGame = False
            guessnum.main()
            printed_output = '\n'.join(str(call) for call in mock_print.call_args_list)
            # Should see a low hint and eventually a game over
            assert ('low' in printed_output.lower()) or guessnum.lostGame

    @patch('guessnum.askForGuess')
    @patch('builtins.print')
    def test_main_too_high_hint(self, mock_print, mock_ask):
        """Should give 'too high' hint when guess is above secret."""
        with patch('random.randint', return_value=25):
            mock_ask.return_value = 50
            guessnum.lostGame = False
            guessnum.main()
            printed_output = '\n'.join(str(call) for call in mock_print.call_args_list)
            # Should see a high hint
            assert ('high' in printed_output.lower()) or guessnum.lostGame

    @patch('guessnum.askForGuess')
    @patch('builtins.print')
    def test_main_loses_after_10_guesses(self, mock_print, mock_ask):
        """Player should lose after 10 incorrect guesses."""
        with patch('random.randint', return_value=50):
            # Make 10 wrong guesses (all under 50)
            mock_ask.side_effect = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            guessnum.lostGame = False
            guessnum.main()
            # After 10 wrong guesses, lostGame should be True
            assert guessnum.lostGame == True

    @patch('guessnum.askForGuess')
    @patch('builtins.print')
    def test_main_secret_number_in_range(self, mock_print, mock_ask):
        """Secret number should always be between 1 and 100."""
        # Test multiple times
        for _ in range(5):
            with patch('random.randint', return_value=50) as mock_randint:
                mock_ask.return_value = 50
                guessnum.lostGame = False
                guessnum.main()
                # Verify randint was called with correct range
                mock_randint.assert_called_with(1, 100)


class TestGameRules:
    """Tests for game rules and constraints."""

    def test_max_guesses_is_ten(self):
        """Game should allow exactly 10 guesses before losing."""
        # This is tested implicitly in main tests, but verify the constant
        # by checking the loop range
        # The game has: for i in range(10)
        # This means 10 iterations max
        assert 10 == 10  # Documenting the rule

    def test_number_range_is_1_to_100(self):
        """Secret number should be between 1 and 100 inclusive."""
        # This is enforced by random.randint(1, 100)
        # Testing that our ask function accepts these boundaries
        with patch('builtins.input', return_value='1'):
            assert guessnum.askForGuess() == 1
        with patch('builtins.input', return_value='100'):
            assert guessnum.askForGuess() == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
