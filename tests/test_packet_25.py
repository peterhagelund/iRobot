"""
Tests for Packet25.
"""


from irobot.packet import Packet25


def test_id():
    """Tests the packet `id`."""
    assert Packet25.id == 25


def test_size():
    """Tests the packet `size`."""
    assert Packet25.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x13, 0x88])
    packet = Packet25.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet25
    assert packet.battery_charge == 5000
