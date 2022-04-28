"""
Tests for Packet13.
"""


from irobot.packet import Packet13


def test_id():
    """Tests the packet `id`."""
    assert Packet13.id == 13


def test_size():
    """Tests the packet `size`."""
    assert Packet13.size == 1


def test_from_bytes_no_virtual_wall():
    """Tests `from_bytes` with no virtual wall seen."""
    data = bytes([0b00000000])
    packet = Packet13.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet13
    assert packet.virtual_wall is False


def test_from_bytes_virtual_wall():
    """Tests `from_bytes` with virtual wall seen."""
    data = bytes([0b00000001])
    packet = Packet13.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet13
    assert packet.virtual_wall is True
