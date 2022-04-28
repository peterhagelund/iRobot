"""
Tests for Packet47.
"""


from irobot.packet import Packet47


def test_id():
    """Tests the packet `id`."""
    assert Packet47.id == 47


def test_size():
    """Tests the packet `size`."""
    assert Packet47.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x06, 0x40])
    packet = Packet47.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet47
    assert packet.bump_front_left_signal == 1600
