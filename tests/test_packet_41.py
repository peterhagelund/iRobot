"""
Tests for Packet41.
"""


from irobot.packet import Packet41


def test_id():
    """Tests the packet `id`."""
    assert Packet41.id == 41


def test_size():
    """Tests the packet `size`."""
    assert Packet41.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0xFF, 0x38])
    packet = Packet41.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet41
    assert packet.requested_right_velocity == -200
