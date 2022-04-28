"""
Tests for Packet46.
"""


from irobot.packet import Packet46


def test_id():
    """Tests the packet `id`."""
    assert Packet46.id == 46


def test_size():
    """Tests the packet `size`."""
    assert Packet46.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x05, 0xdc])
    packet = Packet46.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet46
    assert packet.bump_left_signal == 1500
