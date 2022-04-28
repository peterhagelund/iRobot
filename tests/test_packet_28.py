"""
Tests for Packet28.
"""


from irobot.packet import Packet28


def test_id():
    """Tests the packet `id`."""
    assert Packet28.id == 28


def test_size():
    """Tests the packet `size`."""
    assert Packet28.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x07, 0xd0])
    packet = Packet28.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet28
    assert packet.cliff_left_signal == 2000
