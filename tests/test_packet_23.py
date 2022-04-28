"""
Tests for Packet23.
"""


from irobot.packet import Packet23


def test_id():
    """Tests the packet `id`."""
    assert Packet23.id == 23


def test_size():
    """Tests the packet `size`."""
    assert Packet23.size == 2


def test_from_bytes_running():
    """Tests `from_bytes` with the Roomba charging."""
    data = bytes([0xf0, 0x60])
    packet = Packet23.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet23
    assert packet.current == -4000


def test_from_bytes_charging():
    """Tests `from_bytes` with the Roomba running."""
    data = bytes([0x0f, 0xa0])
    packet = Packet23.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet23
    assert packet.current == 4000
