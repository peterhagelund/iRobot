"""
Tests for Packet55.
"""


from irobot.packet import Packet55


def test_id():
    """Tests the packet `id`."""
    assert Packet55.id == 55


def test_size():
    """Tests the packet `size`."""
    assert Packet55.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0xfc, 0x18])
    packet = Packet55.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet55
    assert packet.right_motor_current == -1000
