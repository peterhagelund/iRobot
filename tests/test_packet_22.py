"""
Tests for Packet22.
"""


from irobot.packet import Packet22


def test_id():
    """Tests the packet `id`."""
    assert Packet22.id == 22


def test_size():
    """Tests the packet `size`."""
    assert Packet22.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x42, 0x68])
    packet = Packet22.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet22
    assert packet.voltage == 17000
