"""
Tests for Packet101.
"""


from irobot.packet import (Packet43, Packet44, Packet45, Packet46, Packet47,
                           Packet48, Packet49, Packet50, Packet51, Packet52,
                           Packet53, Packet54, Packet55, Packet56, Packet57,
                           Packet58, Packet101)


def test_id():
    """Tests the packet `id`."""
    assert Packet101.id == 101


def test_size():
    """Tests the packet `size`."""
    assert Packet101.size == 28


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([
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
    assert len(data) == Packet101.size
    packet = Packet101.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet101
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
