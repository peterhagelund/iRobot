"""
Tests for Packet11.
"""


from irobot.packet import Packet11


def test_id():
    """Tests the packet `id`."""
    assert Packet11.id == 11


def test_size():
    """Tests the packet `size`."""
    assert Packet11.size == 1


def test_from_bytes_no_cliff():
    """Tests `from_bytes` with no cliff seen."""
    data = bytes([0b00000000])
    packet = Packet11.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet11
    assert packet.cliff_front_right is False


def test_from_bytes_cliff():
    """Tests `from_bytes` with cliff seen."""
    data = bytes([0b00000001])
    packet = Packet11.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet11
    assert packet.cliff_front_right is True
