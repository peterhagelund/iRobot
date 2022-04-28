"""
Tests for Packet2.
"""


from irobot.packet import (Packet2, Packet17, Packet18, Packet19, Packet20)


def test_id():
    """Tests the packet `id`."""
    assert Packet2.id == 2


def test_size():
    """Tests the packet `size`."""
    assert Packet2.size == 6


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([
        0x2a,        # Packet 17
        0b10101010,  # Packet 18
        0x01, 0x2c,  # Packet 19
        0xff, 0xa6,  # Packet 20
    ])
    assert len(data) == Packet2.size
    packet = Packet2.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet2
    # Packet 17:
    assert packet.packet_17 is not None
    assert type(packet.packet_17) == Packet17
    assert packet.packet_17.ir_character_omni == 42
    # Packet 18:
    assert packet.packet_18 is not None
    assert type(packet.packet_18) == Packet18
    assert packet.packet_18.clock is True
    assert packet.packet_18.schedule is False
    assert packet.packet_18.day is True
    assert packet.packet_18.hour is False
    assert packet.packet_18.minute is True
    assert packet.packet_18.dock is False
    assert packet.packet_18.spot is True
    assert packet.packet_18.clean is False
    # Packet 19:
    assert packet.packet_19 is not None
    assert type(packet.packet_19) == Packet19
    assert packet.packet_19.distance == 300
    # Packet 20:
    assert packet.packet_20 is not None
    assert type(packet.packet_20) == Packet20
    assert packet.packet_20.angle == -90
