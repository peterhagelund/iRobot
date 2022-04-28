"""
Tests for Packet8.
"""


from irobot.packet import Packet8


def test_id():
    """Tests the packet `id`."""
    assert Packet8.id == 8


def test_size():
    """Tests the packet `size`."""
    assert Packet8.size == 1


def test_from_bytes_no_wall():
    """Tests `from_bytes` with no wall seen."""
    data = bytes([0b00000000])
    packet = Packet8.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet8
    assert packet.wall is False


def test_from_bytes_wall():
    """Tests `from_bytes` with wall seen."""
    data = bytes([0b00000001])
    packet = Packet8.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet8
    assert packet.wall is True
