"""
Tests for Packet9.
"""


from irobot.packet import Packet9


def test_id():
    """Tests the packet `id`."""
    assert Packet9.id == 9


def test_size():
    """Tests the packet `size`."""
    assert Packet9.size == 1


def test_from_bytes_no_cliff():
    """Tests `from_bytes` with no cliff seen."""
    data = bytes([0b00000000])
    packet = Packet9.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet9
    assert packet.cliff_left is False


def test_from_bytes_cliff():
    """Tests `from_bytes` with cliff seen."""
    data = bytes([0b00000001])
    packet = Packet9.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet9
    assert packet.cliff_left is True
