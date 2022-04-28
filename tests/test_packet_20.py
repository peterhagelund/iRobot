"""
Tests for Packet20.
"""


from irobot.packet import Packet20


def test_id():
    """Tests the packet `id`."""
    assert Packet20.id == 20


def test_size():
    """Tests the packet `size`."""
    assert Packet20.size == 2


def test_from_bytes_counter_clockwise():
    """Tests `from_bytes` with a counter-clockwise angle."""
    data = bytes([0x00, 0x5a])
    packet = Packet20.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet20
    assert packet.angle == 90


def test_from_bytes_clockwise():
    """Tests `from_bytes` with a clockwise angle."""
    data = bytes([0xff, 0xa6])
    packet = Packet20.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet20
    assert packet.angle == -90
