"""
Tests for Packet4.
"""


from irobot.packet import (
    Packet4,
    Packet27,
    Packet28,
    Packet29,
    Packet30,
    Packet31,
    Packet32,
    Packet33,
    Packet34,
)


def test_id():
    """Tests the packet `id`."""
    assert Packet4.id == 4


def test_size():
    """Tests the packet `size`."""
    assert Packet4.size == 14


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes(
        [
            0x02,
            0x2B,  # Packet 27
            0x07,
            0xD0,  # Packet 28
            0x08,
            0x34,  # Packet 29
            0x08,
            0x98,  # Packet 30
            0x08,
            0xFC,  # Packet 31
            0x00,  # Packet 32
            0x00,
            0x00,  # Packet 33
            0b00000011,  # Packet 34
        ]
    )
    assert len(data) == Packet4.size
    packet = Packet4.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet4
    # Packet 27:
    assert packet.packet_27 is not None
    assert type(packet.packet_27) == Packet27
    assert packet.packet_27.wall_signal == 555
    # Packet 28:
    assert packet.packet_28 is not None
    assert type(packet.packet_28) == Packet28
    assert packet.packet_28.cliff_left_signal == 2000
    # Packet 29:
    assert packet.packet_29 is not None
    assert type(packet.packet_29) == Packet29
    assert packet.packet_29.cliff_front_left_signal == 2100
    # Packet 30:
    assert packet.packet_30 is not None
    assert type(packet.packet_30) == Packet30
    assert packet.packet_30.cliff_front_right_signal == 2200
    # Packet 31:
    assert packet.packet_31 is not None
    assert type(packet.packet_31) == Packet31
    assert packet.packet_31.cliff_right_signal == 2300
    # Packet 32:
    assert packet.packet_32 is not None
    assert type(packet.packet_32) == Packet32
    assert packet.packet_32.unused_byte == 0
    # Packet 33:
    assert packet.packet_33 is not None
    assert type(packet.packet_33) == Packet33
    assert packet.packet_33.unused_short == 0
    # Packet 34:
    assert packet.packet_34 is not None
    assert type(packet.packet_34) == Packet34
    assert packet.packet_34.home_base is True
    assert packet.packet_34.internal_charger is True
