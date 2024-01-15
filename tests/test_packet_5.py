"""
Tests for Packet5.
"""


from irobot.packet import (
    Mode,
    Packet5,
    Packet35,
    Packet36,
    Packet37,
    Packet38,
    Packet39,
    Packet40,
    Packet41,
    Packet42,
)


def test_id():
    """Tests the packet `id`."""
    assert Packet5.id == 5


def test_size():
    """Tests the packet `size`."""
    assert Packet5.size == 12


def test_from_bytes():
    """Tests `from_bytes`."""
    data = bytes(
        [
            0x02,  # Packet 35
            0x01,  # Packet 36
            0b00000001,  # Packet 37
            0x01,  # Packet 38
            0xFF,
            0x38,  # Packet 39
            0x01,
            0x2C,  # Packet 40
            0xFF,
            0x38,  # Packet 41
            0x00,
            0xC8,  # Packet 42
        ]
    )
    assert len(data) == Packet5.size
    packet = Packet5.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet5
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
