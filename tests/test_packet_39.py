"""
Tests for Packet39.
"""


from irobot.packet import Packet39


def test_id():
    """Tests the packet `id`."""
    assert Packet39.id == 39


def test_size():
    """Tests the packet `size`."""
    assert Packet39.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0xFF, 0x38])
    packet = Packet39.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet39
    assert packet.requested_velocity == -200
