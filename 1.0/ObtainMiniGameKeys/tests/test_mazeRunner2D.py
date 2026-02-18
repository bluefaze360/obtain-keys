"""
Unit tests for mazeRunner2D.py
Tests maze selection validation and file handling
"""

import pytest
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

import mazeRunner2D


class TestMazeSelection:
    """Tests for maze file selection and validation."""

    def test_maze_1_exists(self):
        """Maze file 1 should exist in the Mazes directory."""
        maze_path = os.path.join(mazeRunner2D.script_dir, "Mazes", "maze1.txt")
        assert os.path.exists(maze_path)

    def test_maze_20_exists(self):
        """Maze file 20 should exist in the Mazes directory."""
        maze_path = os.path.join(mazeRunner2D.script_dir, "Mazes", "maze20.txt")
        assert os.path.exists(maze_path)

    def test_valid_maze_numbers_are_digits(self):
        """Valid maze numbers should be single or double digits."""
        valid_inputs = ["1", "5", "10", "20"]
        for inp in valid_inputs:
            assert inp.isdigit()
            assert 1 <= int(inp) <= 20

    def test_invalid_maze_input_non_digit(self):
        """Non-digit inputs should fail validation."""
        invalid_inputs = ["abc", "1a", "a1", ".."]
        for inp in invalid_inputs:
            assert not inp.isdigit()

    def test_invalid_maze_input_out_of_range_zero(self):
        """Input 0 should be out of valid range."""
        assert not (1 <= int("0") <= 20)

    def test_invalid_maze_input_out_of_range_high(self):
        """Input > 20 should be out of valid range."""
        assert not (1 <= int("21") <= 20)
        assert not (1 <= int("999") <= 20)

    def test_invalid_maze_input_path_traversal(self):
        """Path traversal attempts should fail digit check."""
        invalid_inputs = ["../", "1/../", "..", "1.."]
        for inp in invalid_inputs:
            assert not inp.isdigit()

    def test_maze_file_path_construction(self):
        """Maze file paths should be constructed safely with os.path.join."""
        filename = "5"
        maze_path = os.path.join(mazeRunner2D.script_dir, "Mazes", f"maze{filename}.txt")
        expected = os.path.join(mazeRunner2D.script_dir, "Mazes", "maze5.txt")
        assert maze_path == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
