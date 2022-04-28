"""
Tests for Packet56.
"""


from irobot.packet import Packet56


def test_id():
    """Tests the packet `id`."""
    assert Packet56.id == 56


def test_size():
    """Tests the packet `size`."""
    assert Packet56.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x01, 0xf4])
    packet = Packet56.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet56
    assert packet.main_brush_motor_current == 500
