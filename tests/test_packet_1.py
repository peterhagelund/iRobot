"""
Tests for Packet0.
"""


from irobot.packet import (
    Packet1,
    Packet7,
    Packet8,
    Packet9,
    Packet10,
    Packet11,
    Packet12,
    Packet13,
    Packet14,
    Packet15,
    Packet16,
)


def test_id():
    """Tests the packet `id`."""
    assert Packet1.id == 1


def test_size():
    """Tests the packet `size`."""
    assert Packet1.size == 10


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes(
        [
            0b00001010,  # Packet 7
            0b00000001,  # Packet 8
            0b00000001,  # Packet 9
            0b00000000,  # Packet 10
            0b00000001,  # Packet 11
            0b00000000,  # Packet 12
            0b00000001,  # Packet 13
            0b00001000,  # Packet 14
            0x7B,  # Packet 15
            0x00,  # Packet 16
        ]
    )
    assert len(data) == Packet1.size
    packet = Packet1.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet1
    # Packet 7:
    assert packet.packet_7 is not None
    assert type(packet.packet_7) == Packet7
    assert packet.packet_7.wheel_drop_left is True
    assert packet.packet_7.wheel_drop_right is False
    assert packet.packet_7.bump_left is True
    assert packet.packet_7.bump_right is False
    # Packet 8:
    assert packet.packet_8 is not None
    assert type(packet.packet_8) == Packet8
    assert packet.packet_8.wall is True
    # Packet 9:
    assert packet.packet_9 is not None
    assert type(packet.packet_9) == Packet9
    assert packet.packet_9.cliff_left is True
    # Packet 10:
    assert packet.packet_10 is not None
    assert type(packet.packet_10) == Packet10
    assert packet.packet_10.cliff_front_left is False
    # Packet 11:
    assert packet.packet_11 is not None
    assert type(packet.packet_11) == Packet11
    assert packet.packet_11.cliff_front_right is True
    # Packet 12:
    assert packet.packet_12 is not None
    assert type(packet.packet_12) == Packet12
    assert packet.packet_12.cliff_right is False
    # Packet 13:
    assert packet.packet_13 is not None
    assert type(packet.packet_13) == Packet13
    assert packet.packet_13.virtual_wall is True
    # Packet 14:
    assert packet.packet_14 is not None
    assert type(packet.packet_14) == Packet14
    assert packet.packet_14.left_wheel is False
    assert packet.packet_14.right_wheel is True
    assert packet.packet_14.main_brush is False
    assert packet.packet_14.side_brush is False
    # Packet 15:
    assert packet.packet_15 is not None
    assert type(packet.packet_15) == Packet15
    assert packet.packet_15.dirt_detect == 123
    # Packet 16:
    assert packet.packet_16 is not None
    assert type(packet.packet_16) == Packet16
    assert packet.packet_16.unused_byte == 0
