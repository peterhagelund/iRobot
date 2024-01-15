"""
Tests for Packet31.
"""


from irobot.packet import Packet31


def test_id():
    """Tests the packet `id`."""
    assert Packet31.id == 31


def test_size():
    """Tests the packet `size`."""
    assert Packet31.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x08, 0xFC])
    packet = Packet31.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet31
    assert packet.cliff_right_signal == 2300
