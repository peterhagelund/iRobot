"""
Tests for Packet12.
"""


from irobot.packet import Packet12


def test_id():
    """Tests the packet `id`."""
    assert Packet12.id == 12


def test_size():
    """Tests the packet `size`."""
    assert Packet12.size == 1


def test_from_bytes_no_cliff():
    """Tests `from_bytes` with no cliff seen."""
    data = bytes([0b00000000])
    packet = Packet12.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet12
    assert packet.cliff_right is False


def test_from_bytes_cliff():
    """Tests `from_bytes` with cliff seen."""
    data = bytes([0b00000001])
    packet = Packet12.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet12
    assert packet.cliff_right is True
