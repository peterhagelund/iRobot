"""
Tests for Packet26.
"""


from irobot.packet import Packet26


def test_id():
    """Tests the packet `id`."""
    assert Packet26.id == 26


def test_size():
    """Tests the packet `size`."""
    assert Packet26.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x27, 0x10])
    packet = Packet26.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet26
    assert packet.battery_capacity == 10000
