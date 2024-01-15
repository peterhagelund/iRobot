"""
Tests for Packet.
"""


from irobot.packet import (
    Packet,
    Packet0,
    Packet1,
    Packet2,
    Packet3,
    Packet4,
    Packet5,
    Packet6,
    Packet7,
    Packet8,
    Packet9,
    Packet10,
    Packet11,
    Packet12,
    Packet13,
    Packet14,
    Packet15,
    Packet16,
    Packet17,
    Packet18,
    Packet19,
    Packet20,
    Packet21,
    Packet22,
    Packet23,
    Packet24,
    Packet25,
    Packet26,
    Packet27,
    Packet28,
    Packet29,
    Packet30,
    Packet31,
    Packet32,
    Packet33,
    Packet34,
    Packet35,
    Packet36,
    Packet37,
    Packet38,
    Packet39,
    Packet40,
    Packet41,
    Packet42,
    Packet43,
    Packet44,
    Packet45,
    Packet46,
    Packet47,
    Packet48,
    Packet49,
    Packet50,
    Packet51,
    Packet52,
    Packet53,
    Packet54,
    Packet55,
    Packet56,
    Packet57,
    Packet58,
    Packet100,
    Packet101,
    Packet106,
    Packet107,
)


def test_registry():
    """Tests that the packet registry is correctly set up and populated."""
    assert Packet.registry[0] == Packet0
    assert Packet.registry[1] == Packet1
    assert Packet.registry[2] == Packet2
    assert Packet.registry[3] == Packet3
    assert Packet.registry[4] == Packet4
    assert Packet.registry[5] == Packet5
    assert Packet.registry[6] == Packet6
    assert Packet.registry[7] == Packet7
    assert Packet.registry[8] == Packet8
    assert Packet.registry[9] == Packet9
    assert Packet.registry[10] == Packet10
    assert Packet.registry[11] == Packet11
    assert Packet.registry[12] == Packet12
    assert Packet.registry[13] == Packet13
    assert Packet.registry[14] == Packet14
    assert Packet.registry[15] == Packet15
    assert Packet.registry[16] == Packet16
    assert Packet.registry[17] == Packet17
    assert Packet.registry[18] == Packet18
    assert Packet.registry[19] == Packet19
    assert Packet.registry[20] == Packet20
    assert Packet.registry[21] == Packet21
    assert Packet.registry[22] == Packet22
    assert Packet.registry[23] == Packet23
    assert Packet.registry[24] == Packet24
    assert Packet.registry[25] == Packet25
    assert Packet.registry[26] == Packet26
    assert Packet.registry[27] == Packet27
    assert Packet.registry[28] == Packet28
    assert Packet.registry[29] == Packet29
    assert Packet.registry[30] == Packet30
    assert Packet.registry[31] == Packet31
    assert Packet.registry[32] == Packet32
    assert Packet.registry[33] == Packet33
    assert Packet.registry[34] == Packet34
    assert Packet.registry[35] == Packet35
    assert Packet.registry[36] == Packet36
    assert Packet.registry[37] == Packet37
    assert Packet.registry[38] == Packet38
    assert Packet.registry[39] == Packet39
    assert Packet.registry[40] == Packet40
    assert Packet.registry[41] == Packet41
    assert Packet.registry[42] == Packet42
    assert Packet.registry[43] == Packet43
    assert Packet.registry[44] == Packet44
    assert Packet.registry[45] == Packet45
    assert Packet.registry[46] == Packet46
    assert Packet.registry[47] == Packet47
    assert Packet.registry[48] == Packet48
    assert Packet.registry[49] == Packet49
    assert Packet.registry[50] == Packet50
    assert Packet.registry[51] == Packet51
    assert Packet.registry[52] == Packet52
    assert Packet.registry[53] == Packet53
    assert Packet.registry[54] == Packet54
    assert Packet.registry[55] == Packet55
    assert Packet.registry[56] == Packet56
    assert Packet.registry[57] == Packet57
    assert Packet.registry[58] == Packet58
    assert Packet.registry[100] == Packet100
    assert Packet.registry[101] == Packet101
    assert Packet.registry[106] == Packet106
    assert Packet.registry[107] == Packet107
