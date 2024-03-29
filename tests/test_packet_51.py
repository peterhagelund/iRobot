"""
Tests for Packet51.
"""


from irobot.packet import Packet51


def test_id():
    """Tests the packet `id`."""
    assert Packet51.id == 51


def test_size():
    """Tests the packet `size`."""
    assert Packet51.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x07, 0xD0])
    packet = Packet51.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet51
    assert packet.bump_right_signal == 2000
