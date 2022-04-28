"""
Tests for Packet29.
"""


from irobot.packet import Packet29


def test_id():
    """Tests the packet `id`."""
    assert Packet29.id == 29


def test_size():
    """Tests the packet `size`."""
    assert Packet29.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x08, 0x34])
    packet = Packet29.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet29
    assert packet.cliff_front_left_signal == 2100
