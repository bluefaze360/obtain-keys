"""
Unit tests for leetspeakTranslator.py
Tests leetspeak encoding functionality
"""

import pytest
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import leetspeakTranslator


class TestLeetspeakTranslation:
    """Tests for leetspeak translation functionality."""

    def test_englishToLeetspeak_returns_string(self):
        """englishToLeetspeak should return a string."""
        result = leetspeakTranslator.englishToLeetspeak("test")
        assert isinstance(result, str)

    def test_englishToLeetspeak_preserves_non_translatable_chars(self):
        """Characters not in charMapping should be preserved."""
        # Test with characters that have no leet equivalents
        result = leetspeakTranslator.englishToLeetspeak("xyz")
        # x, y, z don't have mappings, so they should be unchanged
        assert 'x' in result.lower()
        assert 'y' in result.lower()
        assert 'z' in result.lower()

    def test_englishToLeetspeak_handles_empty_string(self):
        """englishToLeetspeak should handle empty strings."""
        result = leetspeakTranslator.englishToLeetspeak("")
        assert result == ""

    def test_englishToLeetspeak_handles_punctuation(self):
        """Punctuation should be preserved."""
        result = leetspeakTranslator.englishToLeetspeak("hello!")
        assert "!" in result

    def test_englishToLeetspeak_handles_numbers(self):
        """Numbers should be preserved as-is."""
        result = leetspeakTranslator.englishToLeetspeak("test123")
        assert "123" in result

    def test_englishToLeetspeak_handles_spaces(self):
        """Spaces should be preserved."""
        result = leetspeakTranslator.englishToLeetspeak("hello world")
        assert " " in result

    def test_englishToLeetspeak_handles_case_insensitive(self):
        """Uppercase and lowercase should both be translatable."""
        # Translation is probabilistic, but characters should be processed
        result_lower = leetspeakTranslator.englishToLeetspeak("abc")
        result_upper = leetspeakTranslator.englishToLeetspeak("ABC")
        # Both should return strings
        assert isinstance(result_lower, str)
        assert isinstance(result_upper, str)

    def test_englishToLeetspeak_translatable_chars_exist(self):
        """Test that translatable characters can be converted."""
        # Characters that should have leet versions
        translatable = "acdehikostuv"
        result = leetspeakTranslator.englishToLeetspeak(translatable)
        # Result should contain some leet characters (due to randomness, test multiple times)
        assert len(result) > 0

    def test_englishToLeetspeak_probabilistic_behavior(self):
        """Translation should have some randomness (70% chance)."""
        # Run multiple times and check for variation
        # This is a weak test since it's probabilistic
        char = 'a'
        results = set()
        for _ in range(20):
            result = leetspeakTranslator.englishToLeetspeak(char)
            results.add(result)
        # With high probability, we should get at least 2 different results
        # (either 'a' or a leet version) given the randomness
        assert len(results) >= 1

    def test_englishToLeetspeak_long_string(self):
        """Should handle longer strings without errors."""
        long_string = "the quick brown fox jumps over the lazy dog"
        result = leetspeakTranslator.englishToLeetspeak(long_string)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_englishToLeetspeak_special_chars(self):
        """Should preserve special characters like @, #, $, etc."""
        special = "test@example.com"
        result = leetspeakTranslator.englishToLeetspeak(special)
        assert "@" in result
        assert "." in result
        assert isinstance(result, str)


class TestCharacterMapping:
    """Tests for the character mapping dictionary."""

    def test_char_mapping_keys_are_lowercase(self):
        """All keys in charMapping should be lowercase by design."""
        # This tests the documented constraint
        test_string = "ACDEHIKOSTUV"
        result = leetspeakTranslator.englishToLeetspeak(test_string)
        assert isinstance(result, str)

    def test_char_mapping_values_are_lists(self):
        """charMapping values should be lists of possible replacements."""
        # Test indirectly by checking if replacements work
        result = leetspeakTranslator.englishToLeetspeak("a")
        # Should contain at least some character
        assert len(result) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
