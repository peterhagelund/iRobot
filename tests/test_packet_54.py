"""
Tests for Packet54.
"""


from irobot.packet import Packet54


def test_id():
    """Tests the packet `id`."""
    assert Packet54.id == 54


def test_size():
    """Tests the packet `size`."""
    assert Packet54.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x03, 0xe8])
    packet = Packet54.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet54
    assert packet.left_motor_current == 1000
