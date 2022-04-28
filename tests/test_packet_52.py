"""
Tests for Packet52.
"""


from irobot.packet import Packet52


def test_id():
    """Tests the packet `id`."""
    assert Packet52.id == 52


def test_size():
    """Tests the packet `size`."""
    assert Packet52.size == 1


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([42])
    packet = Packet52.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet52
    assert packet.ir_character_left == 42
