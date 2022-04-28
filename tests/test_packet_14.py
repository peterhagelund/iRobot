"""
Tests for Packet14.
"""


from irobot.packet import Packet14


def test_id():
    """Tests the packet `id`."""
    assert Packet14.id == 14


def test_size():
    """Tests the packet `size`."""
    assert Packet14.size == 1


def test_from_bytes_no_overcurrent():
    """Tests `from_bytes` with no overcurrent detected."""
    data = bytes([0b00000000])
    packet = Packet14.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet14
    assert packet.left_wheel is False
    assert packet.right_wheel is False
    assert packet.main_brush is False
    assert packet.side_brush is False


def test_from_bytes_left_wheel():
    """Tests `from_bytes` with left wheel overcurrent detected."""
    data = bytes([0b00010000])
    packet = Packet14.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet14
    assert packet.left_wheel is True
    assert packet.right_wheel is False
    assert packet.main_brush is False
    assert packet.side_brush is False


def test_from_bytes_right_wheel():
    """Tests `from_bytes` with right wheel overcurrent detected."""
    data = bytes([0b00001000])
    packet = Packet14.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet14
    assert packet.left_wheel is False
    assert packet.right_wheel is True
    assert packet.main_brush is False
    assert packet.side_brush is False


def test_from_bytes_main_brush():
    """Tests `from_bytes` with main brush overcurrent detected."""
    data = bytes([0b00000100])
    packet = Packet14.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet14
    assert packet.left_wheel is False
    assert packet.right_wheel is False
    assert packet.main_brush is True
    assert packet.side_brush is False


def test_from_bytes_side_brush():
    """Tests `from_bytes` with side brush overcurrent detected."""
    data = bytes([0b00000001])
    packet = Packet14.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet14
    assert packet.left_wheel is False
    assert packet.right_wheel is False
    assert packet.main_brush is False
    assert packet.side_brush is True


def test_from_bytes_all_overcurrent():
    """Tests `from_bytes` with overcurrent detected on all motors."""
    data = bytes([0b00011101])
    packet = Packet14.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet14
    assert packet.left_wheel is True
    assert packet.right_wheel is True
    assert packet.main_brush is True
    assert packet.side_brush is True
