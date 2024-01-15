"""
Tests for Packet106.
"""


from irobot.packet import (
    Packet46,
    Packet47,
    Packet48,
    Packet49,
    Packet50,
    Packet51,
    Packet106,
)


def test_id():
    """Tests the packet `id`."""
    assert Packet106.id == 106


def test_size():
    """Tests the packet `size`."""
    assert Packet106.size == 12


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes(
        [
            0x05,
            0xDC,  # Packet 46
            0x06,
            0x40,  # Packet 47
            0x06,
            0xA4,  # Packet 48
            0x07,
            0x08,  # Packet 49
            0x07,
            0x6C,  # Packet 50
            0x07,
            0xD0,  # Packet 51
        ]
    )
    assert len(data) == Packet106.size
    packet = Packet106.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet106
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
