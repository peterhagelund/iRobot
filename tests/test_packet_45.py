"""
Tests for Packet45.
"""


from irobot.packet import Packet45


def test_id():
    """Tests the packet `id`."""
    assert Packet45.id == 45


def test_size():
    """Tests the packet `size`."""
    assert Packet45.size == 1


def test_from_bytes_all_on():
    """Tests `from_bytes` with all bumper lights on."""
    data = bytes([0b00111111])
    packet = Packet45.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet45
    assert packet.bumper_right is True
    assert packet.bumper_front_right is True
    assert packet.bumper_center_right is True
    assert packet.bumper_center_left is True
    assert packet.bumper_front_left is True
    assert packet.bumper_left is True


def test_from_bytes_right_side_on():
    """Tests `from_bytes` with all right bumper lights on."""
    data = bytes([0b00111000])
    packet = Packet45.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet45
    assert packet.bumper_right is True
    assert packet.bumper_front_right is True
    assert packet.bumper_center_right is True
    assert packet.bumper_center_left is False
    assert packet.bumper_front_left is False
    assert packet.bumper_left is False


def test_from_bytes_left_side_on():
    """Tests `from_bytes` with all left bumper lights on."""
    data = bytes([0b00000111])
    packet = Packet45.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet45
    assert packet.bumper_right is False
    assert packet.bumper_front_right is False
    assert packet.bumper_center_right is False
    assert packet.bumper_center_left is True
    assert packet.bumper_front_left is True
    assert packet.bumper_left is True


def test_from_bytes_all_off():
    """Tests `from_bytes` with all bumper lights on."""
    data = bytes([0b00000000])
    packet = Packet45.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet45
    assert packet.bumper_right is False
    assert packet.bumper_front_right is False
    assert packet.bumper_center_right is False
    assert packet.bumper_center_left is False
    assert packet.bumper_front_left is False
    assert packet.bumper_left is False
