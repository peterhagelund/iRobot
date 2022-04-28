"""
Tests for Packet38.
"""


from irobot.packet import Packet38


def test_id():
    """Tests the packet `id`."""
    assert Packet38.id == 38


def test_size():
    """Tests the packet `size`."""
    assert Packet38.size == 1


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x01])
    packet = Packet38.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet38
    assert packet.stream_packet_count == 1
