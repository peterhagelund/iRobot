"""
Tests for Packet53.
"""


from irobot.packet import Packet53


def test_id():
    """Tests the packet `id`."""
    assert Packet53.id == 53


def test_size():
    """Tests the packet `size`."""
    assert Packet53.size == 1


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([42])
    packet = Packet53.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet53
    assert packet.ir_character_right == 42
