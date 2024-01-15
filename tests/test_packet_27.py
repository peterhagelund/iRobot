"""
Tests for Packet27.
"""


from irobot.packet import Packet27


def test_id():
    """Tests the packet `id`."""
    assert Packet27.id == 27


def test_size():
    """Tests the packet `size`."""
    assert Packet27.size == 2


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x02, 0x2B])
    packet = Packet27.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet27
    assert packet.wall_signal == 555
