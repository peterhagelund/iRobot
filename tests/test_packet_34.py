"""
Tests for Packet34.
"""


from irobot.packet import Packet34


def test_id():
    """Tests the packet `id`."""
    assert Packet34.id == 34


def test_size():
    """Tests the packet `size`."""
    assert Packet34.size == 1


def test_from_bytes_none():
    """Tests `from_bytes` with no charging sources available."""
    data = bytes([0b00000000])
    packet = Packet34.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet34
    assert packet.home_base is False
    assert packet.internal_charger is False


def test_from_bytes_home_base():
    """Tests `from_bytes` with home base charging source available."""
    data = bytes([0b00000010])
    packet = Packet34.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet34
    assert packet.home_base is True
    assert packet.internal_charger is False


def test_from_bytes_internal_charger():
    """Tests `from_bytes` with internal charger charging source available."""
    data = bytes([0b00000001])
    packet = Packet34.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet34
    assert packet.home_base is False
    assert packet.internal_charger is True


def test_from_bytes_both():
    """Tests `from_bytes` with both charging sources available."""
    data = bytes([0b000000011])
    packet = Packet34.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet34
    assert packet.home_base is True
    assert packet.internal_charger is True
