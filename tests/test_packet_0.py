"""
Tests for Packet0.
"""


from irobot.packet import (ChargingState, Packet0, Packet7, Packet8, Packet9,
                           Packet10, Packet11, Packet12, Packet13, Packet14,
                           Packet15, Packet16, Packet17, Packet18, Packet19,
                           Packet20, Packet21, Packet22, Packet23, Packet24,
                           Packet25, Packet26)


def test_id():
    """Tests the packet `id`."""
    assert Packet0.id == 0


def test_size():
    """Tests the packet `size`."""
    assert Packet0.size == 26


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([
        0b00001010,  # Packet 7
        0b00000001,  # Packet 8
        0b00000001,  # Packet 9
        0b00000000,  # Packet 10
        0b00000001,  # Packet 11
        0b00000000,  # Packet 12
        0b00000001,  # Packet 13
        0b00001000,  # Packet 14
        0x7b,        # Packet 15
        0x00,        # Packet 16
        0x2a,        # Packet 17
        0b10101010,  # Packet 18
        0x01, 0x2c,  # Packet 19
        0xff, 0xa6,  # Packet 20
        0x02,        # Packet 21
        0x42, 0x68,  # Packet 22
        0xf0, 0x60,  # Packet 23
        0x16,        # Packet 24
        0x13, 0x88,  # Packet 25
        0x27, 0x10,  # Packet 26
    ])
    assert len(data) == Packet0.size
    packet = Packet0.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet0
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
