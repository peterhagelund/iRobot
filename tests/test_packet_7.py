"""
Tests for Packet7.
"""


from irobot.packet import Packet7


def test_id():
    """Tests the packet `id`."""
    assert Packet7.id == 7


def test_size():
    """Tests the packet `size`."""
    assert Packet7.size == 1


def test_from_bytes_all_off():
    """Tests `from_bytes` with all sensors off."""
    data = bytes([0b00000000])
    packet = Packet7.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet7
    assert packet.wheel_drop_left is False
    assert packet.wheel_drop_right is False
    assert packet.bump_left is False
    assert packet.bump_right is False


def test_from_bytes_all_on():
    """Tests `from_bytes` with all sensors on."""
    data = bytes([0b00001111])
    packet = Packet7.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet7
    assert packet.wheel_drop_left is True
    assert packet.wheel_drop_right is True
    assert packet.bump_left is True
    assert packet.bump_right is True


def test_from_bytes_left_on():
    """Tests `from_bytes` with lefthand sensors on."""
    data = bytes([0b00001010])
    packet = Packet7.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet7
    assert packet.wheel_drop_left is True
    assert packet.wheel_drop_right is False
    assert packet.bump_left is True
    assert packet.bump_right is False


def test_from_bytes_right_on():
    """Tests `from_bytes` with righthand sensors on."""
    data = bytes([0b00000101])
    packet = Packet7.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet7
    assert packet.wheel_drop_left is False
    assert packet.wheel_drop_right is True
    assert packet.bump_left is False
    assert packet.bump_right is True
