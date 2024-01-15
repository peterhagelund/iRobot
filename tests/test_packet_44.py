"""
Tests for Packet44.
"""


from irobot.packet import Packet44


def test_id():
    """Tests the packet `id`."""
    assert Packet44.id == 44


def test_size():
    """Tests the packet `size`."""
    assert Packet44.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0xC3, 0x50])
    packet = Packet44.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet44
    assert packet.left_encoder_counts == 50000
