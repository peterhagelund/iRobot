"""
Tests for Packet24.
"""


from irobot.packet import Packet24


def test_id():
    """Tests the packet `id`."""
    assert Packet24.id == 24


def test_size():
    """Tests the packet `size`."""
    assert Packet24.size == 1


def test_from_bytes_winter():
    """Tests `from_bytes` with the Roomba coutside, freezing."""
    data = bytes([0xf6])
    packet = Packet24.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet24
    assert packet.temperature == -10


def test_from_bytes_summer():
    """Tests `from_bytes` with the Roomba inside, warm."""
    data = bytes([0x16])
    packet = Packet24.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet24
    assert packet.temperature == 22
