"""
Tests for Packet33.
"""


from irobot.packet import Packet33


def test_id():
    """Tests the packet `id`."""
    assert Packet33.id == 33


def test_size():
    """Tests the packet `size`."""
    assert Packet33.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0, 0])
    packet = Packet33.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet33
    assert packet.unused_short == 0
