"""
Tests for Packet3.
"""


from irobot.packet import (
    ChargingState,
    Packet3,
    Packet21,
    Packet22,
    Packet23,
    Packet24,
    Packet25,
    Packet26,
)


def test_id():
    """Tests the packet `id`."""
    assert Packet3.id == 3


def test_size():
    """Tests the packet `size`."""
    assert Packet3.size == 10


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes(
        [
            0x02,  # Packet 21
            0x42,
            0x68,  # Packet 22
            0xF0,
            0x60,  # Packet 23
            0x16,  # Packet 24
            0x13,
            0x88,  # Packet 25
            0x27,
            0x10,  # Packet 26
        ]
    )
    assert len(data) == Packet3.size
    packet = Packet3.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet3
    # Packet 21:
    assert packet.packet_21 is not None
    assert type(packet.packet_21) == Packet21
    assert packet.packet_21.charging_state == ChargingState.FULL_CHARGING
    # Packet 22:
    assert packet.packet_22 is not None
    assert type(packet.packet_22) == Packet22
    assert packet.packet_22.voltage == 17000
    # Packet 23:
    assert packet.packet_23 is not None
    assert type(packet.packet_23) == Packet23
    assert packet.packet_23.current == -4000
    # Packet 24:
    assert packet.packet_24 is not None
    assert type(packet.packet_24) == Packet24
    assert packet.packet_24.temperature == 22
    # Packet 25:
    assert packet.packet_25 is not None
    assert type(packet.packet_25) == Packet25
    assert packet.packet_25.battery_charge == 5000
    # Packet 26:
    assert packet.packet_26 is not None
    assert type(packet.packet_26) == Packet26
    assert packet.packet_26.battery_capacity == 10000
