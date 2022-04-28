"""
iRobot packet definitions.

Copyright (c) 2022 Peter Hagelund

License (MIT):

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from abc import ABC, abstractclassmethod
from dataclasses import dataclass
from enum import IntEnum, unique
from struct import unpack_from
from typing import ClassVar, Dict


@unique
class ChargingState(IntEnum):
    """The various Roomba charging states."""
    NOT_CHARGING = 0
    """Roomba is not charging."""
    RECONDITIONING_CHARGING = 1
    """Roomba is reconditioning the battery."""
    FULL_CHARGING = 2
    """Roomba is fully charging the battery."""
    TRICKLE_CHARGING = 3
    """Roomba is trickle charging."""
    WAITING = 4
    """Roomba is waiting to charge."""
    CHARGING_FAULT_CONDITION = 5
    """There is a fault condition."""
    UNKNOWN = 6
    """The charging state is unknow. If the data received from the Roomba is correct, this should never happen."""


@unique
class Mode(IntEnum):
    """The Roomba OI modes."""
    OFF = 0
    """OI is off."""
    PASSIVE = 1
    """OI is in passive mode."""
    SAFE = 2
    """OI is in safe mode."""
    FULL = 3
    """OI is in full mode."""
    UNKNOWN = 4
    """The OI mode is unknown. If the data received from the Roomba is correct, this should never happen."""


class Packet(ABC):
    """Abstract base class for Roomba packts."""
    id: int = None
    """The packet `id`."""
    size: int = None
    """The packet `size`."""
    registry: Dict[str, type]
    """The packet type registry."""

    @staticmethod
    @abstractclassmethod
    def from_bytes(data: bytes, offset: int = 0) -> "Packet":  # pragma: no cover
        """Converts raw bytes, received from a Roomba `sensors` command to the corresponding packet implementation.

        Arguments:
        data: the raw data bytes
        offset: the offset, into the list of data bytes, where the packet data begins

        Return: the `Packet` implementation
        """
        pass


@dataclass
class Packet7(Packet):
    """Roomba packet 7 (Bumps and wheel drops)."""
    id: ClassVar[int] = 7
    size: ClassVar[int] = 1

    wheel_drop_left: bool = False
    wheel_drop_right: bool = False
    bump_left: bool = False
    bump_right: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet7":
        wheel_drop_left = data[offset] & 0b00001000 != 0
        wheel_drop_right = data[offset] & 0b00000100 != 0
        bump_left = data[offset] & 0b00000010 != 0
        bump_right = data[offset] & 0b00000001 != 0
        return Packet7(wheel_drop_left, wheel_drop_right, bump_left, bump_right)


@dataclass
class Packet8(Packet):
    """Roomba packet 8 (Wall)."""
    id: ClassVar[int] = 8
    size: ClassVar[int] = 1

    wall: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet8":
        wall = data[offset] & 0b00000001 != 0
        return Packet8(wall)


@dataclass
class Packet9(Packet):
    """Roomba packet 9 (Cliff left)."""
    id: ClassVar[int] = 9
    size: ClassVar[int] = 1

    cliff_left: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet9":
        cliff_left = data[offset] & 0b00000001 != 0
        return Packet9(cliff_left)


@dataclass
class Packet10(Packet):
    """Roomba packet 10 (Cliff front left)."""
    id: ClassVar[int] = 10
    size: ClassVar[int] = 1

    cliff_front_left: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet10":
        cliff_front_left = data[offset] & 0b00000001 != 0
        return Packet10(cliff_front_left)


@dataclass
class Packet11(Packet):
    """Roomba packet 11 (Cliff front right)."""
    id: ClassVar[int] = 11
    size: ClassVar[int] = 1

    cliff_front_right: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet11":
        cliff_front_right = data[offset] & 0b00000001 != 0
        return Packet11(cliff_front_right)


@dataclass
class Packet12(Packet):
    """Roomba packet 12 (Cliff right)."""
    id: ClassVar[int] = 12
    size: ClassVar[int] = 1

    cliff_right: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet12":
        cliff_right = data[offset] & 0b00000001 != 0
        return Packet12(cliff_right)


@dataclass
class Packet13(Packet):
    """Roomba packet 13 (Virtual wall)."""
    id: ClassVar[int] = 13
    size: ClassVar[int] = 1

    virtual_wall: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet13":
        virtual_wall = data[offset] & 0b00000001 != 0
        return Packet13(virtual_wall)


@dataclass
class Packet14(Packet):
    """Roomba packet 14 (Wheel overcurrents)."""
    id: ClassVar[int] = 14
    size: ClassVar[int] = 1

    left_wheel: bool = False
    right_wheel: bool = False
    main_brush: bool = False
    side_brush: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet14":
        left_wheel = data[offset] & 0b00010000 != 0
        right_wheel = data[offset] & 0b00001000 != 0
        main_brush = data[offset] & 0b00000100 != 0
        side_brush = data[offset] & 0b00000001 != 0
        return Packet14(left_wheel, right_wheel, main_brush, side_brush)


@dataclass
class Packet15(Packet):
    """Roomba packet 15 (Dirt detect)."""
    id: ClassVar[int] = 15
    size: ClassVar[int] = 1

    dirt_detect: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet15":
        dirt_detect, = unpack_from(">B", data, offset=offset)
        return Packet15(dirt_detect)


@dataclass
class Packet16(Packet):
    """Roomba packet 16 (Unused)."""
    id: ClassVar[int] = 16
    size: ClassVar[int] = 1

    unused_byte: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet16":
        unused_byte, = unpack_from(">B", data, offset=offset)
        return Packet16(unused_byte)


@dataclass
class Packet17(Packet):
    """Roomba packet 17 (Infrared character omni)."""
    id: ClassVar[int] = 17
    size: ClassVar[int] = 1

    ir_character_omni: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet17":
        ir_character_omni, = unpack_from(">B", data, offset=offset)
        return Packet17(ir_character_omni)


@dataclass
class Packet18(Packet):
    """Roomba packet 18 (Buttons)."""
    id: ClassVar[int] = 18
    size: ClassVar[int] = 1

    clock: bool = False
    schedule: bool = False
    day: bool = False
    hour: bool = False
    minute: bool = False
    dock: bool = False
    spot: bool = False
    clean: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet18":
        button_bits, = unpack_from(">B", data, offset=offset)
        clock = button_bits & 0b10000000 != 0
        schedule = button_bits & 0b01000000 != 0
        day = button_bits & 0b00100000 != 0
        hour = button_bits & 0b00010000 != 0
        minute = button_bits & 0b00001000 != 0
        dock = button_bits & 0b00000100 != 0
        spot = button_bits & 0b00000010 != 0
        clean = button_bits & 0b00000001 != 0
        return Packet18(clock, schedule, day, hour, minute, dock, spot, clean)


@dataclass
class Packet19(Packet):
    """Roomba packet 19 (Distance)."""
    id: ClassVar[int] = 19
    size: ClassVar[int] = 2

    distance: int

    def from_bytes(data: bytes, offset: int = 0) -> "Packet19":
        distance, = unpack_from(">h", data, offset=offset)
        return Packet19(distance)


@dataclass
class Packet20(Packet):
    """Roomba packet 20 (Angle)."""
    id: ClassVar[int] = 20
    size: ClassVar[int] = 2

    angle: int

    def from_bytes(data: bytes, offset: int = 0) -> "Packet20":
        angle, = unpack_from(">h", data, offset=offset)
        return Packet20(angle)


@dataclass
class Packet21(Packet):
    """Roomba packet 21 (Charging state)."""
    id: ClassVar[int] = 21
    size: ClassVar[int] = 1

    charging_state: ChargingState

    def from_bytes(data: bytes, offset: int = 0) -> "Packet21":
        value, = unpack_from(">B", data, offset=offset)
        try:
            charging_state = ChargingState(value)
        except ValueError:
            charging_state = ChargingState.UNKNOWN
        return Packet21(charging_state)


@dataclass
class Packet22(Packet):
    """Roomba packet 22 (Voltage)."""
    id: ClassVar[int] = 22
    size: ClassVar[int] = 2

    voltage: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet22":
        voltage, = unpack_from(">H", data, offset=offset)
        return Packet22(voltage)


@dataclass
class Packet23(Packet):
    """Roomba packet 23 (Current)."""
    id: ClassVar[int] = 23
    size: ClassVar[int] = 2

    current: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet23":
        current, = unpack_from(">h", data, offset=offset)
        return Packet23(current)


@dataclass
class Packet24(Packet):
    """Roomba packet 23 (Temperature)."""
    id: ClassVar[int] = 24
    size: ClassVar[int] = 1

    temperature: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet23":
        temperature, = unpack_from(">b", data, offset=offset)
        return Packet24(temperature)


@dataclass
class Packet25(Packet):
    """Roomba packet 25 (Battery charge)."""
    id: ClassVar[int] = 25
    size: ClassVar[int] = 2

    battery_charge: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet25":
        battery_charge, = unpack_from(">H", data, offset=offset)
        return Packet25(battery_charge)


@dataclass
class Packet26(Packet):
    """Roomba packet 25 (Battery capacity)."""
    id: ClassVar[int] = 26
    size: ClassVar[int] = 2

    battery_capacity: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet26":
        battery_capacity, = unpack_from(">H", data, offset=offset)
        return Packet26(battery_capacity)


@dataclass
class Packet27(Packet):
    """Roomba packet 27 (Wall signal)."""
    id: ClassVar[int] = 27
    size: ClassVar[int] = 2

    wall_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet27":
        wall_signal, = unpack_from(">H", data, offset=offset)
        return Packet27(wall_signal)


@dataclass
class Packet28(Packet):
    """Roomba packet 28 (Cliff left signal)."""
    id: ClassVar[int] = 28
    size: ClassVar[int] = 2

    cliff_left_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet28":
        cliff_left_signal, = unpack_from(">H", data, offset=offset)
        return Packet28(cliff_left_signal)


@dataclass
class Packet29(Packet):
    """Roomba packet 29 (Cliff front left signal)."""
    id: ClassVar[int] = 29
    size: ClassVar[int] = 2

    cliff_front_left_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet29":
        cliff_front_left_signal, = unpack_from(">H", data, offset=offset)
        return Packet29(cliff_front_left_signal)


@dataclass
class Packet30(Packet):
    """Roomba packet 30 (Cliff front right signal)."""
    id: ClassVar[int] = 30
    size: ClassVar[int] = 2

    cliff_front_right_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet29":
        cliff_front_right_signal, = unpack_from(">H", data, offset=offset)
        return Packet30(cliff_front_right_signal)


@dataclass
class Packet31(Packet):
    """Roomba packet 31 (Cliff right signal)."""
    id: ClassVar[int] = 31
    size: ClassVar[int] = 2

    cliff_right_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet28":
        cliff_right_signal, = unpack_from(">H", data, offset=offset)
        return Packet31(cliff_right_signal)


@dataclass
class Packet32(Packet):
    """Roomba packet 32 (Unused)."""
    id: ClassVar[int] = 32
    size: ClassVar[int] = 1

    unused_byte: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet32":
        unused_byte, = unpack_from(">B", data, offset=offset)
        return Packet32(unused_byte)


@dataclass
class Packet33(Packet):
    """Roomba packet 33 (Unused)."""
    id: ClassVar[int] = 33
    size: ClassVar[int] = 2

    unused_short: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet33":
        unused_short, = unpack_from(">H", data, offset=offset)
        return Packet33(unused_short)


@dataclass
class Packet34(Packet):
    """Roomba packet 34 (Charging sources available)."""
    id: ClassVar[int] = 34
    size: ClassVar[int] = 1

    home_base: bool = False
    internal_charger: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet34":
        source_bits, = unpack_from(">B", data, offset=offset)
        home_base = source_bits & 0b00000010 != 0
        internal_charger = source_bits & 0b00000001 != 0
        return Packet34(home_base, internal_charger)


@dataclass
class Packet35(Packet):
    """Roomba packet 35 (OI mode)."""
    id: ClassVar[int] = 35
    size: ClassVar[int] = 1

    mode: Mode = Mode.OFF

    def from_bytes(data: bytes, offset: int = 0) -> "Packet35":
        value, = unpack_from(">B", data, offset=offset)
        try:
            mode = Mode(value)
        except ValueError:
            mode = Mode.UNKNOWN
        return Packet35(mode)


@dataclass
class Packet36(Packet):
    """Roomba packet 36 (Song number)."""
    id: ClassVar[int] = 36
    size: ClassVar[int] = 1

    song: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet36":
        song, = unpack_from(">B", data, offset=offset)
        return Packet36(song)


@dataclass
class Packet37(Packet):
    """Roomba packet 37 (Song playing)."""
    id: ClassVar[int] = 37
    size: ClassVar[int] = 1

    song_playing: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet37":
        song_bits, = unpack_from(">B", data, offset=offset)
        song = song_bits & 0b00000001 != 0
        return Packet37(song)


@dataclass
class Packet38(Packet):
    """Roomba packet 38 (Number of stream packets)."""
    id: ClassVar[int] = 38
    size: ClassVar[int] = 1

    stream_packet_count: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet38":
        stream_packet_count, = unpack_from(">B", data, offset=offset)
        return Packet38(stream_packet_count)


@dataclass
class Packet39(Packet):
    """Roomba packet 39 (Requested velocity)."""
    id: ClassVar[int] = 39
    size: ClassVar[int] = 2

    requested_velocity: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet39":
        requested_velocity, = unpack_from(">h", data, offset=offset)
        return Packet39(requested_velocity)


@dataclass
class Packet40(Packet):
    """Roomba packet 40 (Requested radius)."""
    id: ClassVar[int] = 40
    size: ClassVar[int] = 2

    requested_radius: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet40":
        requested_radius, = unpack_from(">h", data, offset=offset)
        return Packet40(requested_radius)


@dataclass
class Packet41(Packet):
    """Roomba packet 41 (Requested right velocity)."""
    id: ClassVar[int] = 41
    size: ClassVar[int] = 2

    requested_right_velocity: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet41":
        requested_right_velocity, = unpack_from(">h", data, offset=offset)
        return Packet41(requested_right_velocity)


@dataclass
class Packet42(Packet):
    """Roomba packet 42 (Requested left velocity)."""
    id: ClassVar[int] = 42
    size: ClassVar[int] = 2

    requested_left_velocity: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet42":
        requested_left_velocity, = unpack_from(">h", data, offset=offset)
        return Packet42(requested_left_velocity)


@dataclass
class Packet43(Packet):
    """Roomba packet 43 (Right encoder counts)."""
    id: ClassVar[int] = 43
    size: ClassVar[int] = 2

    right_encoder_counts: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet43":
        right_encoder_counts, = unpack_from(">H", data, offset=offset)
        return Packet43(right_encoder_counts)


@dataclass
class Packet44(Packet):
    """Roomba packet 44 (Left encoder counts)."""
    id: ClassVar[int] = 44
    size: ClassVar[int] = 2

    left_encoder_counts: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet44":
        left_encoder_counts, = unpack_from(">H", data, offset=offset)
        return Packet44(left_encoder_counts)


@dataclass
class Packet45(Packet):
    """Roomba packet 45 (Light bumper)."""
    id: ClassVar[int] = 45
    size: ClassVar[int] = 1

    bumper_right: bool = False
    bumper_front_right: bool = False
    bumper_center_right: bool = False
    bumper_center_left: bool = False
    bumper_front_left: bool = False
    bumper_left: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet45":
        bumper_bits, = unpack_from(">B", data, offset=offset)
        bumper_right = bumper_bits & 0b00100000 != 0
        bumper_front_right = bumper_bits & 0b00010000 != 0
        bumper_center_right = bumper_bits & 0b00001000 != 0
        bumper_center_left = bumper_bits & 0b00000100 != 0
        bumper_front_left = bumper_bits & 0b00000010 != 0
        bumper_left = bumper_bits & 0b00000001 != 0
        return Packet45(bumper_right, bumper_front_right, bumper_center_right, bumper_center_left, bumper_front_left, bumper_left)


@dataclass
class Packet46(Packet):
    """Roomba packet 46 (Light bump left signal)."""
    id: ClassVar[int] = 46
    size: ClassVar[int] = 2

    bump_left_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet46":
        bump_left_signal, = unpack_from(">H", data, offset=offset)
        return Packet46(bump_left_signal)


@dataclass
class Packet47(Packet):
    """Roomba packet 47 (Light bump front left signal)."""
    id: ClassVar[int] = 47
    size: ClassVar[int] = 2

    bump_front_left_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet47":
        bump_front_left_signal, = unpack_from(">H", data, offset=offset)
        return Packet47(bump_front_left_signal)


@dataclass
class Packet48(Packet):
    """Roomba packet 48 (Light bump center left signal)."""
    id: ClassVar[int] = 48
    size: ClassVar[int] = 2

    bump_center_left_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet48":
        bump_center_left_signal, = unpack_from(">H", data, offset=offset)
        return Packet48(bump_center_left_signal)


@dataclass
class Packet49(Packet):
    """Roomba packet 49 (Light bump center right signal)."""
    id: ClassVar[int] = 49
    size: ClassVar[int] = 2

    bump_center_right_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet49":
        bump_center_right_signal, = unpack_from(">H", data, offset=offset)
        return Packet49(bump_center_right_signal)


@dataclass
class Packet50(Packet):
    """Roomba packet 50 (Light bump front right signal)."""
    id: ClassVar[int] = 50
    size: ClassVar[int] = 2

    bump_front_right_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet50":
        bump_front_right_signal, = unpack_from(">H", data, offset=offset)
        return Packet50(bump_front_right_signal)


@dataclass
class Packet51(Packet):
    """Roomba packet 51 (Light bump right signal)."""
    id: ClassVar[int] = 51
    size: ClassVar[int] = 2

    bump_right_signal: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet51":
        bump_right_signal, = unpack_from(">H", data, offset=offset)
        return Packet51(bump_right_signal)


@dataclass
class Packet52(Packet):
    """Roomba packet 52 (Infrared character left)."""
    id: ClassVar[int] = 52
    size: ClassVar[int] = 1

    ir_character_left: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet52":
        ir_character_left, = unpack_from(">B", data, offset=offset)
        return Packet52(ir_character_left)


@dataclass
class Packet53(Packet):
    """Roomba packet 53 (Infrared character right)."""
    id: ClassVar[int] = 53
    size: ClassVar[int] = 1

    ir_character_right: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet53":
        ir_character_right, = unpack_from(">B", data, offset=offset)
        return Packet53(ir_character_right)


@dataclass
class Packet54(Packet):
    """Roomba packet 54 (Left motor current)."""
    id: ClassVar[int] = 54
    size: ClassVar[int] = 2

    left_motor_current: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet54":
        left_motor_current, = unpack_from(">h", data, offset=offset)
        return Packet54(left_motor_current)


@dataclass
class Packet55(Packet):
    """Roomba packet 55 (Right motor current)."""
    id: ClassVar[int] = 55
    size: ClassVar[int] = 2

    right_motor_current: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet55":
        right_motor_current, = unpack_from(">h", data, offset=offset)
        return Packet55(right_motor_current)


@dataclass
class Packet56(Packet):
    """Roomba packet 56 (Main brush motor current)."""
    id: ClassVar[int] = 56
    size: ClassVar[int] = 2

    main_brush_motor_current: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet56":
        main_brush_motor_current, = unpack_from(">h", data, offset=offset)
        return Packet56(main_brush_motor_current)


@dataclass
class Packet57(Packet):
    """Roomba packet 57 (Side brush motor current)."""
    id: ClassVar[int] = 57
    size: ClassVar[int] = 2

    side_brush_motor_current: int = 0

    def from_bytes(data: bytes, offset: int = 0) -> "Packet57":
        side_brush_motor_current, = unpack_from(">h", data, offset=offset)
        return Packet57(side_brush_motor_current)


@dataclass
class Packet58(Packet):
    """Roomba packet 58 (Stasis)."""
    id: ClassVar[int] = 58
    size: ClassVar[int] = 1

    forward_progress: bool = False

    def from_bytes(data: bytes, offset: int = 0) -> "Packet58":
        stasis_bits, = unpack_from(">B", data, offset=offset)
        forward_progress = stasis_bits & 0b00000001 != 0
        return Packet58(forward_progress)


@dataclass
class Packet0(Packet):
    """Roomba packet 0 (Group packet for packets 7 to 26)."""
    id: ClassVar[int] = 0
    size: ClassVar[int] = 26

    packet_7: Packet7
    packet_8: Packet8
    packet_9: Packet9
    packet_10: Packet10
    packet_11: Packet11
    packet_12: Packet12
    packet_13: Packet13
    packet_14: Packet14
    packet_15: Packet15
    packet_16: Packet16
    packet_17: Packet17
    packet_18: Packet18
    packet_19: Packet19
    packet_20: Packet20
    packet_21: Packet21
    packet_22: Packet22
    packet_23: Packet23
    packet_24: Packet24
    packet_25: Packet25
    packet_26: Packet26

    def from_bytes(data: bytes, offset: int = 0) -> "Packet0":
        packet_7 = Packet7.from_bytes(data, offset=offset)
        offset += Packet7.size
        packet_8 = Packet8.from_bytes(data, offset=offset)
        offset += Packet8.size
        packet_9 = Packet9.from_bytes(data, offset=offset)
        offset += Packet9.size
        packet_10 = Packet10.from_bytes(data, offset=offset)
        offset += Packet10.size
        packet_11 = Packet11.from_bytes(data, offset=offset)
        offset += Packet11.size
        packet_12 = Packet12.from_bytes(data, offset=offset)
        offset += Packet12.size
        packet_13 = Packet13.from_bytes(data, offset=offset)
        offset += Packet13.size
        packet_14 = Packet14.from_bytes(data, offset=offset)
        offset += Packet14.size
        packet_15 = Packet15.from_bytes(data, offset=offset)
        offset += Packet15.size
        packet_16 = Packet16.from_bytes(data, offset=offset)
        offset += Packet16.size
        packet_17 = Packet17.from_bytes(data, offset=offset)
        offset += Packet17.size
        packet_18 = Packet18.from_bytes(data, offset=offset)
        offset += Packet18.size
        packet_19 = Packet19.from_bytes(data, offset=offset)
        offset += Packet19.size
        packet_20 = Packet20.from_bytes(data, offset=offset)
        offset += Packet20.size
        packet_21 = Packet21.from_bytes(data, offset=offset)
        offset += Packet21.size
        packet_22 = Packet22.from_bytes(data, offset=offset)
        offset += Packet22.size
        packet_23 = Packet23.from_bytes(data, offset=offset)
        offset += Packet23.size
        packet_24 = Packet24.from_bytes(data, offset=offset)
        offset += Packet24.size
        packet_25 = Packet25.from_bytes(data, offset=offset)
        offset += Packet25.size
        packet_26 = Packet26.from_bytes(data, offset=offset)

        return Packet0(packet_7, packet_8, packet_9,
                       packet_10, packet_11, packet_12, packet_13, packet_14, packet_15, packet_16, packet_17, packet_18, packet_19,
                       packet_20, packet_21, packet_22, packet_23, packet_24, packet_25, packet_26)


@dataclass
class Packet1(Packet):
    """Roomba packet 1 (Group packet for packets 7 to 16)."""
    id: ClassVar[int] = 1
    size: ClassVar[int] = 10

    packet_7: Packet7
    packet_8: Packet8
    packet_9: Packet9
    packet_10: Packet10
    packet_11: Packet11
    packet_12: Packet12
    packet_13: Packet13
    packet_14: Packet14
    packet_15: Packet15
    packet_16: Packet16

    def from_bytes(data: bytes, offset: int = 0) -> "Packet1":
        packet_7 = Packet7.from_bytes(data, offset=offset)
        offset += Packet7.size
        packet_8 = Packet8.from_bytes(data, offset=offset)
        offset += Packet8.size
        packet_9 = Packet9.from_bytes(data, offset=offset)
        offset += Packet9.size
        packet_10 = Packet10.from_bytes(data, offset=offset)
        offset += Packet10.size
        packet_11 = Packet11.from_bytes(data, offset=offset)
        offset += Packet11.size
        packet_12 = Packet12.from_bytes(data, offset=offset)
        offset += Packet12.size
        packet_13 = Packet13.from_bytes(data, offset=offset)
        offset += Packet13.size
        packet_14 = Packet14.from_bytes(data, offset=offset)
        offset += Packet14.size
        packet_15 = Packet15.from_bytes(data, offset=offset)
        offset += Packet15.size
        packet_16 = Packet16.from_bytes(data, offset=offset)

        return Packet1(packet_7, packet_8, packet_9,
                       packet_10, packet_11, packet_12, packet_13, packet_14, packet_15, packet_16)


@dataclass
class Packet2(Packet):
    """Roomba packet 2 (Group packet for packets 17 to 20)."""
    id: ClassVar[int] = 2
    size: ClassVar[int] = 6

    packet_17: Packet17
    packet_18: Packet18
    packet_19: Packet19
    packet_20: Packet20

    def from_bytes(data: bytes, offset: int = 0) -> "Packet2":
        packet_17 = Packet17.from_bytes(data, offset=offset)
        offset += Packet17.size
        packet_18 = Packet18.from_bytes(data, offset=offset)
        offset += Packet18.size
        packet_19 = Packet19.from_bytes(data, offset=offset)
        offset += Packet19.size
        packet_20 = Packet20.from_bytes(data, offset=offset)

        return Packet2(packet_17, packet_18, packet_19, packet_20)


@dataclass
class Packet3(Packet):
    """Roomba packet 3 (Group packet for packets 21 to 26)."""
    id: ClassVar[int] = 3
    size: ClassVar[int] = 10

    packet_21: Packet21
    packet_22: Packet22
    packet_23: Packet23
    packet_24: Packet24
    packet_25: Packet25
    packet_26: Packet26

    def from_bytes(data: bytes, offset: int = 0) -> "Packet3":
        packet_21 = Packet21.from_bytes(data, offset=offset)
        offset += Packet21.size
        packet_22 = Packet22.from_bytes(data, offset=offset)
        offset += Packet22.size
        packet_23 = Packet23.from_bytes(data, offset=offset)
        offset += Packet23.size
        packet_24 = Packet24.from_bytes(data, offset=offset)
        offset += Packet24.size
        packet_25 = Packet25.from_bytes(data, offset=offset)
        offset += Packet25.size
        packet_26 = Packet26.from_bytes(data, offset=offset)

        return Packet3(packet_21, packet_22, packet_23, packet_24, packet_25, packet_26)


@dataclass
class Packet4(Packet):
    """Roomba packet 4 (Group packet for packets 27 to 34)."""
    id: ClassVar[int] = 4
    size: ClassVar[int] = 14

    packet_27: Packet27
    packet_28: Packet28
    packet_29: Packet29
    packet_30: Packet30
    packet_31: Packet31
    packet_32: Packet32
    packet_33: Packet33
    packet_34: Packet34

    def from_bytes(data: bytes, offset: int = 0) -> "Packet4":
        packet_27 = Packet27.from_bytes(data, offset=offset)
        offset += Packet27.size
        packet_28 = Packet28.from_bytes(data, offset=offset)
        offset += Packet28.size
        packet_29 = Packet29.from_bytes(data, offset=offset)
        offset += Packet29.size
        packet_30 = Packet30.from_bytes(data, offset=offset)
        offset += Packet30.size
        packet_31 = Packet31.from_bytes(data, offset=offset)
        offset += Packet31.size
        packet_32 = Packet32.from_bytes(data, offset=offset)
        offset += Packet32.size
        packet_33 = Packet33.from_bytes(data, offset=offset)
        offset += Packet33.size
        packet_34 = Packet34.from_bytes(data, offset=offset)
        return Packet4(packet_27, packet_28, packet_29, packet_30, packet_31, packet_32, packet_33, packet_34)


@dataclass
class Packet5(Packet):
    """Roomba packet 5 (Group packet for packets 35 to 42)."""
    id: ClassVar[int] = 5
    size: ClassVar[int] = 12

    packet_35: Packet35
    packet_36: Packet36
    packet_37: Packet37
    packet_38: Packet38
    packet_39: Packet39
    packet_40: Packet40
    packet_41: Packet41
    packet_42: Packet42

    def from_bytes(data: bytes, offset: int = 0) -> "Packet5":
        packet_35 = Packet35.from_bytes(data, offset=offset)
        offset += Packet35.size
        packet_36 = Packet36.from_bytes(data, offset=offset)
        offset += Packet36.size
        packet_37 = Packet37.from_bytes(data, offset=offset)
        offset += Packet37.size
        packet_38 = Packet38.from_bytes(data, offset=offset)
        offset += Packet38.size
        packet_39 = Packet39.from_bytes(data, offset=offset)
        offset += Packet39.size
        packet_40 = Packet40.from_bytes(data, offset=offset)
        offset += Packet40.size
        packet_41 = Packet41.from_bytes(data, offset=offset)
        offset += Packet41.size
        packet_42 = Packet42.from_bytes(data, offset=offset)
        return Packet5(packet_35, packet_36, packet_37, packet_38, packet_39, packet_40, packet_41, packet_42)


@dataclass
class Packet6(Packet):
    """Roomba packet 6 (Group packet for packets 7 to 42)."""
    id: ClassVar[int] = 6
    size: ClassVar[int] = 52

    packet_7: Packet7
    packet_8: Packet8
    packet_9: Packet9
    packet_10: Packet10
    packet_11: Packet11
    packet_12: Packet12
    packet_13: Packet13
    packet_14: Packet14
    packet_15: Packet15
    packet_16: Packet16
    packet_17: Packet17
    packet_18: Packet18
    packet_19: Packet19
    packet_20: Packet20
    packet_21: Packet21
    packet_22: Packet22
    packet_23: Packet23
    packet_24: Packet24
    packet_25: Packet25
    packet_26: Packet26
    packet_27: Packet27
    packet_28: Packet28
    packet_29: Packet29
    packet_30: Packet30
    packet_31: Packet31
    packet_32: Packet32
    packet_33: Packet33
    packet_34: Packet34
    packet_35: Packet35
    packet_36: Packet36
    packet_37: Packet37
    packet_38: Packet38
    packet_39: Packet39
    packet_40: Packet40
    packet_41: Packet41
    packet_42: Packet42

    def from_bytes(data: bytes, offset: int = 0) -> "Packet0":
        packet_7 = Packet7.from_bytes(data, offset=offset)
        offset += Packet7.size
        packet_8 = Packet8.from_bytes(data, offset=offset)
        offset += Packet8.size
        packet_9 = Packet9.from_bytes(data, offset=offset)
        offset += Packet9.size
        packet_10 = Packet10.from_bytes(data, offset=offset)
        offset += Packet10.size
        packet_11 = Packet11.from_bytes(data, offset=offset)
        offset += Packet11.size
        packet_12 = Packet12.from_bytes(data, offset=offset)
        offset += Packet12.size
        packet_13 = Packet13.from_bytes(data, offset=offset)
        offset += Packet13.size
        packet_14 = Packet14.from_bytes(data, offset=offset)
        offset += Packet14.size
        packet_15 = Packet15.from_bytes(data, offset=offset)
        offset += Packet15.size
        packet_16 = Packet16.from_bytes(data, offset=offset)
        offset += Packet16.size
        packet_17 = Packet17.from_bytes(data, offset=offset)
        offset += Packet17.size
        packet_18 = Packet18.from_bytes(data, offset=offset)
        offset += Packet18.size
        packet_19 = Packet19.from_bytes(data, offset=offset)
        offset += Packet19.size
        packet_20 = Packet20.from_bytes(data, offset=offset)
        offset += Packet20.size
        packet_21 = Packet21.from_bytes(data, offset=offset)
        offset += Packet21.size
        packet_22 = Packet22.from_bytes(data, offset=offset)
        offset += Packet22.size
        packet_23 = Packet23.from_bytes(data, offset=offset)
        offset += Packet23.size
        packet_24 = Packet24.from_bytes(data, offset=offset)
        offset += Packet24.size
        packet_25 = Packet25.from_bytes(data, offset=offset)
        offset += Packet25.size
        packet_26 = Packet26.from_bytes(data, offset=offset)
        offset += Packet26.size
        packet_27 = Packet27.from_bytes(data, offset=offset)
        offset += Packet27.size
        packet_28 = Packet28.from_bytes(data, offset=offset)
        offset += Packet28.size
        packet_29 = Packet29.from_bytes(data, offset=offset)
        offset += Packet29.size
        packet_30 = Packet30.from_bytes(data, offset=offset)
        offset += Packet30.size
        packet_31 = Packet31.from_bytes(data, offset=offset)
        offset += Packet31.size
        packet_32 = Packet32.from_bytes(data, offset=offset)
        offset += Packet32.size
        packet_33 = Packet33.from_bytes(data, offset=offset)
        offset += Packet33.size
        packet_34 = Packet34.from_bytes(data, offset=offset)
        offset += Packet34.size
        packet_35 = Packet35.from_bytes(data, offset=offset)
        offset += Packet35.size
        packet_36 = Packet36.from_bytes(data, offset=offset)
        offset += Packet36.size
        packet_37 = Packet37.from_bytes(data, offset=offset)
        offset += Packet37.size
        packet_38 = Packet38.from_bytes(data, offset=offset)
        offset += Packet38.size
        packet_39 = Packet39.from_bytes(data, offset=offset)
        offset += Packet39.size
        packet_40 = Packet40.from_bytes(data, offset=offset)
        offset += Packet40.size
        packet_41 = Packet41.from_bytes(data, offset=offset)
        offset += Packet41.size
        packet_42 = Packet42.from_bytes(data, offset=offset)

        return Packet6(packet_7, packet_8, packet_9,
                       packet_10, packet_11, packet_12, packet_13, packet_14, packet_15, packet_16, packet_17, packet_18, packet_19,
                       packet_20, packet_21, packet_22, packet_23, packet_24, packet_25, packet_26, packet_27, packet_28, packet_29,
                       packet_30, packet_31, packet_32, packet_33, packet_34, packet_35, packet_36, packet_37, packet_38, packet_39,
                       packet_40, packet_41, packet_42)


@dataclass
class Packet100(Packet):
    """Roomba packet 100 (Group packet for packets 7 to 58)."""
    id: ClassVar[int] = 100
    size: ClassVar[int] = 80

    packet_7: Packet7
    packet_8: Packet8
    packet_9: Packet9
    packet_10: Packet10
    packet_11: Packet11
    packet_12: Packet12
    packet_13: Packet13
    packet_14: Packet14
    packet_15: Packet15
    packet_16: Packet16
    packet_17: Packet17
    packet_18: Packet18
    packet_19: Packet19
    packet_20: Packet20
    packet_21: Packet21
    packet_22: Packet22
    packet_23: Packet23
    packet_24: Packet24
    packet_25: Packet25
    packet_26: Packet26
    packet_27: Packet27
    packet_28: Packet28
    packet_29: Packet29
    packet_30: Packet30
    packet_31: Packet31
    packet_32: Packet32
    packet_33: Packet33
    packet_34: Packet34
    packet_35: Packet35
    packet_36: Packet36
    packet_37: Packet37
    packet_38: Packet38
    packet_39: Packet39
    packet_40: Packet40
    packet_41: Packet41
    packet_42: Packet42
    packet_43: Packet43
    packet_44: Packet44
    packet_45: Packet45
    packet_46: Packet46
    packet_47: Packet47
    packet_48: Packet48
    packet_49: Packet49
    packet_50: Packet50
    packet_51: Packet51
    packet_52: Packet52
    packet_53: Packet53
    packet_54: Packet54
    packet_55: Packet55
    packet_56: Packet56
    packet_57: Packet57
    packet_58: Packet58

    def from_bytes(data: bytes, offset: int = 0) -> "Packet100":
        packet_7 = Packet7.from_bytes(data, offset=offset)
        offset += Packet7.size
        packet_8 = Packet8.from_bytes(data, offset=offset)
        offset += Packet8.size
        packet_9 = Packet9.from_bytes(data, offset=offset)
        offset += Packet9.size
        packet_10 = Packet10.from_bytes(data, offset=offset)
        offset += Packet10.size
        packet_11 = Packet11.from_bytes(data, offset=offset)
        offset += Packet11.size
        packet_12 = Packet12.from_bytes(data, offset=offset)
        offset += Packet12.size
        packet_13 = Packet13.from_bytes(data, offset=offset)
        offset += Packet13.size
        packet_14 = Packet14.from_bytes(data, offset=offset)
        offset += Packet14.size
        packet_15 = Packet15.from_bytes(data, offset=offset)
        offset += Packet15.size
        packet_16 = Packet16.from_bytes(data, offset=offset)
        offset += Packet16.size
        packet_17 = Packet17.from_bytes(data, offset=offset)
        offset += Packet17.size
        packet_18 = Packet18.from_bytes(data, offset=offset)
        offset += Packet18.size
        packet_19 = Packet19.from_bytes(data, offset=offset)
        offset += Packet19.size
        packet_20 = Packet20.from_bytes(data, offset=offset)
        offset += Packet20.size
        packet_21 = Packet21.from_bytes(data, offset=offset)
        offset += Packet21.size
        packet_22 = Packet22.from_bytes(data, offset=offset)
        offset += Packet22.size
        packet_23 = Packet23.from_bytes(data, offset=offset)
        offset += Packet23.size
        packet_24 = Packet24.from_bytes(data, offset=offset)
        offset += Packet24.size
        packet_25 = Packet25.from_bytes(data, offset=offset)
        offset += Packet25.size
        packet_26 = Packet26.from_bytes(data, offset=offset)
        offset += Packet26.size
        packet_27 = Packet27.from_bytes(data, offset=offset)
        offset += Packet27.size
        packet_28 = Packet28.from_bytes(data, offset=offset)
        offset += Packet28.size
        packet_29 = Packet29.from_bytes(data, offset=offset)
        offset += Packet29.size
        packet_30 = Packet30.from_bytes(data, offset=offset)
        offset += Packet30.size
        packet_31 = Packet31.from_bytes(data, offset=offset)
        offset += Packet31.size
        packet_32 = Packet32.from_bytes(data, offset=offset)
        offset += Packet32.size
        packet_33 = Packet33.from_bytes(data, offset=offset)
        offset += Packet33.size
        packet_34 = Packet34.from_bytes(data, offset=offset)
        offset += Packet34.size
        packet_35 = Packet35.from_bytes(data, offset=offset)
        offset += Packet35.size
        packet_36 = Packet36.from_bytes(data, offset=offset)
        offset += Packet36.size
        packet_37 = Packet37.from_bytes(data, offset=offset)
        offset += Packet37.size
        packet_38 = Packet38.from_bytes(data, offset=offset)
        offset += Packet38.size
        packet_39 = Packet39.from_bytes(data, offset=offset)
        offset += Packet39.size
        packet_40 = Packet40.from_bytes(data, offset=offset)
        offset += Packet40.size
        packet_41 = Packet41.from_bytes(data, offset=offset)
        offset += Packet41.size
        packet_42 = Packet42.from_bytes(data, offset=offset)
        offset += Packet42.size
        packet_43 = Packet43.from_bytes(data, offset=offset)
        offset += Packet43.size
        packet_44 = Packet44.from_bytes(data, offset=offset)
        offset += Packet44.size
        packet_45 = Packet45.from_bytes(data, offset=offset)
        offset += Packet45.size
        packet_46 = Packet46.from_bytes(data, offset=offset)
        offset += Packet46.size
        packet_47 = Packet47.from_bytes(data, offset=offset)
        offset += Packet47.size
        packet_48 = Packet48.from_bytes(data, offset=offset)
        offset += Packet48.size
        packet_49 = Packet49.from_bytes(data, offset=offset)
        offset += Packet49.size
        packet_50 = Packet50.from_bytes(data, offset=offset)
        offset += Packet50.size
        packet_51 = Packet51.from_bytes(data, offset=offset)
        offset += Packet51.size
        packet_52 = Packet52.from_bytes(data, offset=offset)
        offset += Packet52.size
        packet_53 = Packet53.from_bytes(data, offset=offset)
        offset += Packet53.size
        packet_54 = Packet54.from_bytes(data, offset=offset)
        offset += Packet54.size
        packet_55 = Packet55.from_bytes(data, offset=offset)
        offset += Packet55.size
        packet_56 = Packet56.from_bytes(data, offset=offset)
        offset += Packet56.size
        packet_57 = Packet57.from_bytes(data, offset=offset)
        offset += Packet57.size
        packet_58 = Packet58.from_bytes(data, offset=offset)

        return Packet100(packet_7, packet_8, packet_9,
                         packet_10, packet_11, packet_12, packet_13, packet_14, packet_15, packet_16, packet_17, packet_18, packet_19,
                         packet_20, packet_21, packet_22, packet_23, packet_24, packet_25, packet_26, packet_27, packet_28, packet_29,
                         packet_30, packet_31, packet_32, packet_33, packet_34, packet_35, packet_36, packet_37, packet_38, packet_39,
                         packet_40, packet_41, packet_42, packet_43,  packet_44, packet_45, packet_46, packet_47, packet_48, packet_49,
                         packet_50, packet_51, packet_52, packet_53, packet_54, packet_55, packet_56, packet_57, packet_58)


@dataclass
class Packet101(Packet):
    """Roomba packet 101 (Group packet for packets 43 to 58)."""
    id: ClassVar[int] = 101
    size: ClassVar[int] = 28

    packet_43: Packet43
    packet_44: Packet44
    packet_45: Packet45
    packet_46: Packet46
    packet_47: Packet47
    packet_48: Packet48
    packet_49: Packet49
    packet_50: Packet50
    packet_51: Packet51
    packet_52: Packet52
    packet_53: Packet53
    packet_54: Packet54
    packet_55: Packet55
    packet_56: Packet56
    packet_57: Packet57
    packet_58: Packet58

    def from_bytes(data: bytes, offset: int = 0) -> "Packet101":
        packet_43 = Packet43.from_bytes(data, offset=offset)
        offset += Packet43.size
        packet_44 = Packet44.from_bytes(data, offset=offset)
        offset += Packet44.size
        packet_45 = Packet45.from_bytes(data, offset=offset)
        offset += Packet45.size
        packet_46 = Packet46.from_bytes(data, offset=offset)
        offset += Packet46.size
        packet_47 = Packet47.from_bytes(data, offset=offset)
        offset += Packet47.size
        packet_48 = Packet48.from_bytes(data, offset=offset)
        offset += Packet48.size
        packet_49 = Packet49.from_bytes(data, offset=offset)
        offset += Packet49.size
        packet_50 = Packet50.from_bytes(data, offset=offset)
        offset += Packet50.size
        packet_51 = Packet51.from_bytes(data, offset=offset)
        offset += Packet51.size
        packet_52 = Packet52.from_bytes(data, offset=offset)
        offset += Packet52.size
        packet_53 = Packet53.from_bytes(data, offset=offset)
        offset += Packet53.size
        packet_54 = Packet54.from_bytes(data, offset=offset)
        offset += Packet54.size
        packet_55 = Packet55.from_bytes(data, offset=offset)
        offset += Packet55.size
        packet_56 = Packet56.from_bytes(data, offset=offset)
        offset += Packet56.size
        packet_57 = Packet57.from_bytes(data, offset=offset)
        offset += Packet57.size
        packet_58 = Packet58.from_bytes(data, offset=offset)
        return Packet101(packet_43,  packet_44, packet_45, packet_46, packet_47, packet_48, packet_49,
                         packet_50, packet_51, packet_52, packet_53, packet_54, packet_55, packet_56, packet_57, packet_58)


@dataclass
class Packet106(Packet):
    """Roomba packet 106 (Group packet for packets 46 to 51)."""
    id: ClassVar[int] = 106
    size: ClassVar[int] = 12

    packet_46: Packet46
    packet_47: Packet47
    packet_48: Packet48
    packet_49: Packet49
    packet_50: Packet50
    packet_51: Packet51

    def from_bytes(data: bytes, offset: int = 0) -> "Packet106":
        packet_46 = Packet46.from_bytes(data, offset=offset)
        offset += Packet46.size
        packet_47 = Packet47.from_bytes(data, offset=offset)
        offset += Packet47.size
        packet_48 = Packet48.from_bytes(data, offset=offset)
        offset += Packet48.size
        packet_49 = Packet49.from_bytes(data, offset=offset)
        offset += Packet49.size
        packet_50 = Packet50.from_bytes(data, offset=offset)
        offset += Packet50.size
        packet_51 = Packet51.from_bytes(data, offset=offset)
        return Packet106(packet_46, packet_47, packet_48, packet_49, packet_50, packet_51)


@dataclass
class Packet107(Packet):
    """Roomba packet 107 (Group packet for packets 54 to 58)."""
    id: ClassVar[int] = 107
    size: ClassVar[int] = 9

    packet_54: Packet54
    packet_55: Packet55
    packet_56: Packet56
    packet_57: Packet57
    packet_58: Packet58

    def from_bytes(data: bytes, offset: int = 0) -> "Packet107":
        packet_54 = Packet54.from_bytes(data, offset=offset)
        offset += Packet54.size
        packet_55 = Packet55.from_bytes(data, offset=offset)
        offset += Packet55.size
        packet_56 = Packet56.from_bytes(data, offset=offset)
        offset += Packet56.size
        packet_57 = Packet57.from_bytes(data, offset=offset)
        offset += Packet57.size
        packet_58 = Packet58.from_bytes(data, offset=offset)
        return Packet107(packet_54, packet_55, packet_56, packet_57, packet_58)


Packet.registry = {
    0: Packet0,
    1: Packet1,
    2: Packet2,
    3: Packet3,
    4: Packet4,
    5: Packet5,
    6: Packet6,
    7: Packet7,
    8: Packet8,
    9: Packet9,
    10: Packet10,
    11: Packet11,
    12: Packet12,
    13: Packet13,
    14: Packet14,
    15: Packet15,
    16: Packet16,
    17: Packet17,
    18: Packet18,
    19: Packet19,
    20: Packet20,
    21: Packet21,
    22: Packet22,
    23: Packet23,
    24: Packet24,
    25: Packet25,
    26: Packet26,
    27: Packet27,
    28: Packet28,
    29: Packet29,
    30: Packet30,
    31: Packet31,
    32: Packet32,
    33: Packet33,
    34: Packet34,
    35: Packet35,
    36: Packet36,
    37: Packet37,
    38: Packet38,
    39: Packet39,
    40: Packet40,
    41: Packet41,
    42: Packet42,
    43: Packet43,
    44: Packet44,
    45: Packet45,
    46: Packet46,
    47: Packet47,
    48: Packet48,
    49: Packet49,
    50: Packet50,
    51: Packet51,
    52: Packet52,
    53: Packet53,
    54: Packet54,
    55: Packet55,
    56: Packet56,
    57: Packet57,
    58: Packet58,
    100: Packet100,
    101: Packet101,
    106: Packet106,
    107: Packet107,
}
