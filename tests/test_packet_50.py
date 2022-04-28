"""
Tests for Packet50.
"""


from irobot.packet import Packet50


def test_id():
    """Tests the packet `id`."""
    assert Packet50.id == 50


def test_size():
    """Tests the packet `size`."""
    assert Packet50.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x07, 0x6c])
    packet = Packet50.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet50
    assert packet.bump_front_right_signal == 1900
