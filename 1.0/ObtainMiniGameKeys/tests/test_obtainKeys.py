"""
Unit tests for obtainKeys.py
Tests core data loading, inventory management, and file I/O
"""

import pytest
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

import obtainKeys


class TestDataLoading:
    """Tests for reading and parsing game data files."""

    def test_readRoomFile_returns_list(self):
        """readRoomFile should return a non-empty list."""
        result = obtainKeys.readRoomFile()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_readRoomFile_records_have_required_fields(self):
        """Each room record should have at least room ID and description."""
        result = obtainKeys.readRoomFile()
        for record in result:
            assert isinstance(record, list)
            assert len(record) >= 2  # At least [room_id, description]

    def test_readMapFile_returns_list(self):
        """readMapFile should return a non-empty list."""
        result = obtainKeys.readMapFile()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_readMapFile_records_have_required_fields(self):
        """Each map record should have destination, direction, origin, etc."""
        result = obtainKeys.readMapFile()
        for record in result:
            assert isinstance(record, list)
            assert len(record) >= 3  # At least [destination, direction, origin]

    def test_readObjFile_returns_list(self):
        """readObjFile should return a non-empty list."""
        result = obtainKeys.readObjFile()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_readObjFile_records_have_required_fields(self):
        """Each object record should have object name and room location."""
        result = obtainKeys.readObjFile()
        for record in result:
            assert isinstance(record, list)
            assert len(record) >= 2  # At least [object_name, room]

    def test_readGameFile_returns_list(self):
        """readGameFile should return a non-empty list."""
        result = obtainKeys.readGameFile()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_readGameFile_records_have_required_fields(self):
        """Each game record should have game name and room location."""
        result = obtainKeys.readGameFile()
        for record in result:
            assert isinstance(record, list)
            assert len(record) >= 2  # At least [game_name, room]

    def test_readFiles_returns_four_lists(self):
        """readFiles should return exactly four lists (room, map, obj, game)."""
        result = obtainKeys.readFiles()
        assert isinstance(result, tuple)
        assert len(result) == 4
        for item in result:
            assert isinstance(item, list)


class TestInventoryManagement:
    """Tests for inventory management functions."""

    def test_manageInv_adds_item(self):
        """manageInv should add an item to the items list."""
        obtainKeys.items = []
        obtainKeys.manageInv("test_item")
        assert "test_item" in obtainKeys.items

    def test_manageInv_deduplicates(self):
        """manageInv should not add duplicate items."""
        obtainKeys.items = []
        obtainKeys.manageInv("test_item")
        obtainKeys.manageInv("test_item")
        assert obtainKeys.items.count("test_item") == 1

    def test_manageInv_keeps_items_sorted(self):
        """manageInv should keep the items list sorted."""
        obtainKeys.items = []
        obtainKeys.manageInv("zebra")
        obtainKeys.manageInv("apple")
        obtainKeys.manageInv("banana")
        assert obtainKeys.items == ["apple", "banana", "zebra"]

    def test_manageInv_multiple_different_items(self):
        """manageInv should handle multiple different items correctly."""
        obtainKeys.items = []
        items_to_add = ["key_A", "key_B", "torch", "defuser"]
        for item in items_to_add:
            obtainKeys.manageInv(item)
        assert len(obtainKeys.items) == 4
        assert obtainKeys.items == sorted(items_to_add)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
