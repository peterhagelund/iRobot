"""
Tests for Packet21.
"""


from irobot.packet import ChargingState, Packet21


def test_id():
    """Tests the packet `id`."""
    assert Packet21.id == 21


def test_size():
    """Tests the packet `size`."""
    assert Packet21.size == 1


def test_from_bytes_valid_state():
    """Tests `from_bytes` with a valid charging state."""
    data = bytes([0x02])
    packet = Packet21.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet21
    assert packet.charging_state == ChargingState.FULL_CHARGING


def test_from_bytes_unknown_state():
    """Tests `from_bytes` with an unknown charging state."""
    data = bytes([0x0a])
    packet = Packet21.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet21
    assert packet.charging_state == ChargingState.UNKNOWN
