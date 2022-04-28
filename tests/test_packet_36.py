"""
Tests for Packet36.
"""


from irobot.packet import Packet36


def test_id():
    """Tests the packet `id`."""
    assert Packet36.id == 36


def test_size():
    """Tests the packet `size`."""
    assert Packet36.size == 1


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x01])
    packet = Packet36.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet36
    assert packet.song == 1
