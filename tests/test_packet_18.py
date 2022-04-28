"""
Tests for Packet18.
"""


from irobot.packet import Packet18


def test_id():
    """Tests the packet `id`."""
    assert Packet18.id == 18


def test_size():
    """Tests the packet `size`."""
    assert Packet18.size == 1


def test_from_bytes():
    """Tests `from_bytes` with various buttons on/off."""
    data = bytes([0b10101010])
    packet = Packet18.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet18
    assert packet.clock is True
    assert packet.schedule is False
    assert packet.day is True
    assert packet.hour is False
    assert packet.minute is True
    assert packet.dock is False
    assert packet.spot is True
    assert packet.clean is False


def test_from_bytes_all_on():
    """Tests `from_bytes` with all buttons on."""
    data = bytes([0b11111111])
    packet = Packet18.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet18
    assert packet.clock is True
    assert packet.schedule is True
    assert packet.day is True
    assert packet.hour is True
    assert packet.minute is True
    assert packet.dock is True
    assert packet.spot is True
    assert packet.clean is True


def test_from_bytes_all_off():
    """Tests `from_bytes` with all buttons off."""
    data = bytes([0b00000000])
    packet = Packet18.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet18
    assert packet.clock is False
    assert packet.schedule is False
    assert packet.day is False
    assert packet.hour is False
    assert packet.minute is False
    assert packet.dock is False
    assert packet.spot is False
    assert packet.clean is False
