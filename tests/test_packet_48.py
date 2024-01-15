"""
Tests for Packet48.
"""


from irobot.packet import Packet48


def test_id():
    """Tests the packet `id`."""
    assert Packet48.id == 48


def test_size():
    """Tests the packet `size`."""
    assert Packet48.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x06, 0xA4])
    packet = Packet48.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet48
    assert packet.bump_center_left_signal == 1700
