"""
Tests for Packet40.
"""


from irobot.packet import Packet40


def test_id():
    """Tests the packet `id`."""
    assert Packet40.id == 40


def test_size():
    """Tests the packet `size`."""
    assert Packet40.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x01, 0x2C])
    packet = Packet40.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet40
    assert packet.requested_radius == 300
