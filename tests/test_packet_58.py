"""
Tests for Packet58.
"""


from irobot.packet import Packet58


def test_id():
    """Tests the packet `id`."""
    assert Packet58.id == 58


def test_size():
    """Tests the packet `size`."""
    assert Packet58.size == 1


def test_from_bytes_forward_progress():
    """Tests `from_bytes`."""
    data = bytes([0b00000001])
    packet = Packet58.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet58
    assert packet.forward_progress is True


def test_from_bytes_no_forward_progress():
    """Tests `from_bytes`."""
    data = bytes([0b00000000])
    packet = Packet58.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet58
    assert packet.forward_progress is False
