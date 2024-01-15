"""
Tests for Packet17.
"""


from irobot.packet import Packet17


def test_id():
    """Tests the packet `id`."""
    assert Packet17.id == 17


def test_size():
    """Tests the packet `size`."""
    assert Packet17.size == 1


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([0x2A])
    packet = Packet17.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet17
    assert packet.ir_character_omni == 42
