"""
Tests for Packet107.
"""


from irobot.packet import (Packet54, Packet55, Packet56, Packet57, Packet58,
                           Packet107)


def test_id():
    """Tests the packet `id`."""
    assert Packet107.id == 107


def test_size():
    """Tests the packet `size`."""
    assert Packet107.size == 9


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes([
        0x03, 0xe8,  # Packet 54
        0xfc, 0x18,  # Packet 55
        0x01, 0xf4,  # Packet 56
        0x01, 0x2c,  # Packet 57
        0b00000001,  # Packet 58
    ])
    assert len(data) == Packet107.size
    packet = Packet107.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet107
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
