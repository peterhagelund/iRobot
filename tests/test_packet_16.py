"""
Tests for Packet16.
"""


from irobot.packet import Packet16


def test_id():
    """Tests the packet `id`."""
    assert Packet16.id == 16


def test_size():
    """Tests the packet `size`."""
    assert Packet16.size == 1


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x00])
    packet = Packet16.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet16
    assert packet.unused_byte == 0
