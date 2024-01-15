"""
Tests for Packet19.
"""


from irobot.packet import Packet19


def test_id():
    """Tests the packet `id`."""
    assert Packet19.id == 19


def test_size():
    """Tests the packet `size`."""
    assert Packet19.size == 2


def test_from_bytes_forward():
    """Tests `from_bytes` with a forward distance."""
    data = bytes([0x01, 0x2C])
    packet = Packet19.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet19
    assert packet.distance == 300


def test_from_bytes_backward():
    """Tests `from_bytes` with a backward distance."""
    data = bytes([0xFF, 0xC8])
    packet = Packet19.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet19
    assert packet.distance == -56
