"""
Tests for Packet35.
"""


from irobot.packet import Mode, Packet35


def test_id():
    """Tests the packet `id`."""
    assert Packet35.id == 35


def test_size():
    """Tests the packet `size`."""
    assert Packet35.size == 1


def test_from_bytes_valid_mode():
    """Tests `from_bytes` with a valid OI mode."""
    data = bytes([0x02])
    packet = Packet35.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet35
    assert packet.mode == Mode.SAFE


def test_from_bytes_unknown_mode():
    """Tests `from_bytes` with an unknown OI mode."""
    data = bytes([0x0a])
    packet = Packet35.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet35
    assert packet.mode == Mode.UNKNOWN
