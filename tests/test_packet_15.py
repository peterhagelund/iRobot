"""
Tests for Packet15.
"""


from irobot.packet import Packet15


def test_id():
    """Tests the packet `id`."""
    assert Packet15.id == 15


def test_size():
    """Tests the packet `size`."""
    assert Packet15.size == 1


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x7b])
    packet = Packet15.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet15
    assert packet.dirt_detect == 123
