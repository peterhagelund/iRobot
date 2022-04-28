"""
Tests for Packet43.
"""


from irobot.packet import Packet43


def test_id():
    """Tests the packet `id`."""
    assert Packet43.id == 43


def test_size():
    """Tests the packet `size`."""
    assert Packet43.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x9c, 0x40])
    packet = Packet43.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet43
    assert packet.right_encoder_counts == 40000
