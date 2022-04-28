"""
Tests for Packet30.
"""


from irobot.packet import Packet30


def test_id():
    """Tests the packet `id`."""
    assert Packet30.id == 30


def test_size():
    """Tests the packet `size`."""
    assert Packet30.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x08, 0x98])
    packet = Packet30.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet30
    assert packet.cliff_front_right_signal == 2200
