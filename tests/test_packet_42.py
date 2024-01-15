"""
Tests for Packet42.
"""


from irobot.packet import Packet42


def test_id():
    """Tests the packet `id`."""
    assert Packet42.id == 42


def test_size():
    """Tests the packet `size`."""
    assert Packet42.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x00, 0xC8])
    packet = Packet42.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet42
    assert packet.requested_left_velocity == 200
