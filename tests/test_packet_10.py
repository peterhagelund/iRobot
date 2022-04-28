"""
Tests for Packet10.
"""


from irobot.packet import Packet10


def test_id():
    """Tests the packet `id`."""
    assert Packet10.id == 10


def test_size():
    """Tests the packet `size`."""
    assert Packet10.size == 1


def test_from_bytes_no_cliff():
    """Tests `from_bytes` with no cliff seen."""
    data = bytes([0b00000000])
    packet = Packet10.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet10
    assert packet.cliff_front_left is False


def test_from_bytes_cliff():
    """Tests `from_bytes` with cliff seen."""
    data = bytes([0b00000001])
    packet = Packet10.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet10
    assert packet.cliff_front_left is True
