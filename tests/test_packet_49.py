"""
Tests for Packet49.
"""


from irobot.packet import Packet49


def test_id():
    """Tests the packet `id`."""
    assert Packet49.id == 49


def test_size():
    """Tests the packet `size`."""
    assert Packet49.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x07, 0x08])
    packet = Packet49.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet49
    assert packet.bump_center_right_signal == 1800
