"""
Tests for Packet100.
"""


from irobot.packet import (ChargingState, Mode, Packet7, Packet8, Packet9,
                           Packet10, Packet11, Packet12, Packet13, Packet14,
                           Packet15, Packet16, Packet17, Packet18, Packet19,
                           Packet20, Packet21, Packet22, Packet23, Packet24,
                           Packet25, Packet26, Packet27, Packet28, Packet29,
                           Packet30, Packet31, Packet32, Packet33, Packet34,
                           Packet35, Packet36, Packet37, Packet38, Packet39,
                           Packet40, Packet41, Packet42, Packet43, Packet44,
                           Packet45, Packet46, Packet47, Packet48, Packet49,
                           Packet50, Packet51, Packet52, Packet53, Packet54,
                           Packet55, Packet56, Packet57, Packet58, Packet100)


def test_id():
    """Tests the packet `id`."""
    assert Packet100.id == 100


def test_size():
    """Tests the packet `size`."""
    assert Packet100.size == 80


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
        0x02, 0x2b,  # Packet 27
        0x07, 0xd0,  # Packet 28
        0x08, 0x34,  # Packet 29
        0x08, 0x98,  # Packet 30
        0x08, 0xfc,  # Packet 31
        0x00,        # Packet 32
        0x00, 0x00,  # Packet 33
        0b00000011,  # Packet 34
        0x02,        # Packet 35
        0x01,        # Packet 36
        0b00000001,  # Packet 37
        0x01,        # Packet 38
        0xff, 0x38,  # Packet 39
        0x01, 0x2c,  # Packet 40
        0xff, 0x38,  # Packet 41
        0x00, 0xc8,  # Packet 42
        0x9c, 0x40,  # Packet 43
        0xc3, 0x50,  # Packet 44
        0b00111111,  # Packet 45
        0x05, 0xdc,  # Packet 46
        0x06, 0x40,  # Packet 47
        0x06, 0xa4,  # Packet 48
        0x07, 0x08,  # Packet 49
        0x07, 0x6c,  # Packet 50
        0x07, 0xd0,  # Packet 51
        42,          # Packet 52
        42,          # Packet 53
        0x03, 0xe8,  # Packet 54
        0xfc, 0x18,  # Packet 55
        0x01, 0xf4,  # Packet 56
        0x01, 0x2c,  # Packet 57
        0b00000001,  # Packet 58
    ])
    assert len(data) == Packet100.size
    packet = Packet100.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet100
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
    # Packet 35:
    assert packet.packet_35 is not None
    assert type(packet.packet_35) == Packet35
    assert packet.packet_35.mode == Mode.SAFE
    # Packet 36:
    assert packet.packet_36 is not None
    assert type(packet.packet_36) == Packet36
    assert packet.packet_36.song == 1
    # Packet 37:
    assert packet.packet_37 is not None
    assert type(packet.packet_37) == Packet37
    assert packet.packet_37.song_playing is True
    # Packet 38:
    assert packet.packet_38 is not None
    assert type(packet.packet_38) == Packet38
    assert packet.packet_38.stream_packet_count == 1
    # Packet 39:
    assert packet.packet_39 is not None
    assert type(packet.packet_39) == Packet39
    assert packet.packet_39.requested_velocity == -200
    # Packet 40:
    assert packet.packet_40 is not None
    assert type(packet.packet_40) == Packet40
    assert packet.packet_40.requested_radius == 300
    # Packet 41:
    assert packet.packet_41 is not None
    assert type(packet.packet_41) == Packet41
    assert packet.packet_41.requested_right_velocity == -200
    # Packet 42:
    assert packet.packet_42 is not None
    assert type(packet.packet_42) == Packet42
    assert packet.packet_42.requested_left_velocity == 200
    # Packet 43:
    assert packet.packet_43 is not None
    assert type(packet.packet_43) == Packet43
    assert packet.packet_43.right_encoder_counts == 40000
    # Packet 44:
    assert packet.packet_44 is not None
    assert type(packet.packet_44) == Packet44
    assert packet.packet_44.left_encoder_counts == 50000
    # Packet 45:
    assert packet.packet_45 is not None
    assert type(packet.packet_45) == Packet45
    assert packet.packet_45.bumper_right is True
    assert packet.packet_45.bumper_front_right is True
    assert packet.packet_45.bumper_center_right is True
    assert packet.packet_45.bumper_center_left is True
    assert packet.packet_45.bumper_front_left is True
    assert packet.packet_45.bumper_left is True
    # Packet 46:
    assert packet.packet_46 is not None
    assert type(packet.packet_46) == Packet46
    assert packet.packet_46.bump_left_signal == 1500
    # Packet 47:
    assert packet.packet_47 is not None
    assert type(packet.packet_47) == Packet47
    assert packet.packet_47.bump_front_left_signal == 1600
    # Packet 48:
    assert packet.packet_48 is not None
    assert type(packet.packet_48) == Packet48
    assert packet.packet_48.bump_center_left_signal == 1700
    # Packet 49:
    assert packet.packet_49 is not None
    assert type(packet.packet_49) == Packet49
    assert packet.packet_49.bump_center_right_signal == 1800
    # Packet 50:
    assert packet.packet_50 is not None
    assert type(packet.packet_50) == Packet50
    assert packet.packet_50.bump_front_right_signal == 1900
    # Packet 51:
    assert packet.packet_51 is not None
    assert type(packet.packet_51) == Packet51
    assert packet.packet_51.bump_right_signal == 2000
    # Packet 52:
    assert packet.packet_52 is not None
    assert type(packet.packet_52) == Packet52
    assert packet.packet_52.ir_character_left == 42
    # Packet 53:
    assert packet.packet_53 is not None
    assert type(packet.packet_53) == Packet53
    assert packet.packet_53.ir_character_right == 42
    # Packet 54:
    assert packet.packet_54 is not None
    assert type(packet.packet_54) == Packet54
    assert packet.packet_54.left_motor_current == 1000
    # Packet 55:
    assert packet.packet_55 is not None
    assert type(packet.packet_55) == Packet55
    assert packet.packet_55.right_motor_current == -1000
    # Packet 56:
    assert packet.packet_56 is not None
    assert type(packet.packet_56) == Packet56
    assert packet.packet_56.main_brush_motor_current == 500
    # Packet 57:
    assert packet.packet_57 is not None
    assert type(packet.packet_57) == Packet57
    assert packet.packet_57.side_brush_motor_current == 300
    # Packet 58:
    assert packet.packet_58 is not None
    assert type(packet.packet_58) == Packet58
    assert packet.packet_58.forward_progress is True
