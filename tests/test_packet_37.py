"""
Tests for Packet37.
"""


from irobot.packet import Packet37


def test_id():
    """Tests the packet `id`."""
    assert Packet37.id == 37


def test_size():
    """Tests the packet `size`."""
    assert Packet37.size == 1


def test_from_bytes_no_song_playing():
    """Tests `from_bytes` with no song playing."""
    data = bytes([0b00000000])
    packet = Packet37.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet37
    assert packet.song_playing is False


def test_from_bytes_song_playing():
    """Tests `from_bytes` with a song playing."""
    data = bytes([0b00000001])
    packet = Packet37.from_bytes(data)
    assert packet is not None
    assert type(packet) == Packet37
    assert packet.song_playing is True
