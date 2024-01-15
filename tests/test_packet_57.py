"""
Tests for Packet57.
"""


from irobot.packet import Packet57


def test_id():
    """Tests the packet `id`."""
    assert Packet57.id == 57


def test_size():
    """Tests the packet `size`."""
    assert Packet57.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x01, 0x2C])
    packet = Packet57.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet57
    assert packet.side_brush_motor_current == 300
