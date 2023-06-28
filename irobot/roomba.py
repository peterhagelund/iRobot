"""
iRobot Roomba.

Copyright (c) 2022, 2023 Peter Hagelund

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


from datetime import datetime
from enum import IntEnum, unique
from io import StringIO
from logging import DEBUG, Logger
from struct import pack
from threading import Lock
from time import sleep
from typing import List, Self, Tuple

from serial import Serial

from irobot.packet import Packet
from irobot.util import hex_dump

START_DURATION = 0.5
"""The delay after a `START` command."""
MODE_CHANGE_DURATION = 50 / 1000
"""The delay after a mode change command."""
COMMAND_PROCESS_DURATION = 25 / 1000
"""Standard command processing delay."""


@unique
class Command(IntEnum):
    """Supported Roomba commands."""

    START = 128
    """The `START` command. Must be executed before any other commands are sent."""
    BAUD = 129
    """The `BAUD` command. Changes the OI's baud rate."""
    CONTROL = 130
    """The `CONTROL` command. Does the same thing as `SAFE`."""
    SAFE = 131
    """The `SAFE` command. Changes the OI's mode to safe."""
    FULL = 132
    """The `FULL` command. Changes the OI's mode to full."""
    POWER = 133
    """The `POWER` command. Powers down the Roomba."""
    SPOT = 134
    """The `SPOT` command. Starts a 'spot' cleaning cycle."""
    CLEAN = 135
    """The `CLEAN` command. Starts the default cleaning cycle."""
    MAX = 136
    """The `MAX` command. Starts a 'max' cleaning cycle."""
    DRIVE = 137
    """The `DRIVE` command. Instructs the Roomba to drive (use `DRIVE_DIRECT` or `DRIVE_PWM` instead)."""
    MOTORS = 138
    """The `MOTORS` command Instructs the Roomba to turns its motors on and off (use `MOTORS_PWM` instead)."""
    LEDS = 139
    """The `LEDS` command. Instructs the Roomba to turn its LEDs on and off."""
    SONG = 140
    """The `SONG` command. Defines a song of up to 16 notes."""
    PLAY = 141
    """The `PLAY` command. Plays a song."""
    SENSORS = 142
    """The `SENSORS` command. Instructs the Roomba to return a packet with one or more sensor values."""
    SEEK_DOCK = 143
    """The `SEEK_DOCK` command. Instructs the Roomba to seek its dock."""
    MOTORS_PWM = 144
    """The `MOTORS_PWM` command. Instructs the Roomba to turn its motors on and off using raw PWM values."""
    DRIVE_DIRECT = 145
    """The `DRIVE_DIRECT` command. Instructs the Roomba to drive using direct left and right velocites."""
    DRIVE_PWM = 146
    """The `DRIVE_PWM` command. Instructs the Roomba to drive using raw PWM values."""
    STREAM = 148
    """The `STREAM` command. Instructs the Roomba to stream sensor packets."""
    QUERY_LIST = 149
    """The `QUERY_LIST` command. Instructs the Roomba to return a list of sensor packets."""
    PAUSE_RESUME_STREAM = 150
    """The `PAUSE_RESUME_STREAM` command. Instructs the Roomba to start or stop streaming."""
    SCHEDULING_LEDS = 162
    """The `SCHEDULING_LEDS` command. Instructs the Roomba to turns its scheduling LEDs on and off."""
    DIGIT_LEDS_RAW = 163
    """The `DIGIT_LEDS_RAW` command. Instructs the Roomba to turn its scheduling LEDs on and off using raw values."""
    DIGIT_LEDS_ASCII = 164
    """The `DIGIT_LEDS_ASCII` command. Instructs the Roomba to turn its scheduling LEDS on and off using ASCII text."""
    BUTTONS = 165
    """The `BUTTONS` command. Presses one or more Roomba buttons."""
    SCHEDULE = 167
    """The `SCHEDULE` command. Creates a cleaning schedule."""
    SET_DAY_TIME = 168
    """The `SET_DAY_TIME` command. Sets the Roomba's internal week day and time."""


@unique
class BaudCode(IntEnum):
    """Supported Roomba baud rates."""

    B300 = 0
    """300 baud."""
    B600 = 1
    """600 baud."""
    B1200 = 2
    """1200 baud."""
    B2400 = 3
    """2400 baud."""
    B4800 = 4
    """4800 baud."""
    B9600 = 5
    """9600 baud."""
    B14400 = 6
    """14,400 baud."""
    B19200 = 7
    """19,200 baud (can be set during power-on)."""
    B28800 = 8
    """28,800 baud."""
    B38400 = 9
    """38,400 baud."""
    B57600 = 10
    """57,600 baud."""
    B115200 = 11
    """115,200 baud (the default for modern Roombas)."""


@unique
class WeekDay(IntEnum):
    """Roomba week days."""

    SUNDAY = 0
    """Sunday."""
    MONDAY = 1
    """Monday."""
    TUESDAY = 2
    """Tuesday."""
    WEDNESDAY = 3
    """Wednesday."""
    THURSDAY = 4
    """Thursday."""
    FRIDAY = 5
    """Friday."""
    SATURDAY = 6
    """Saturday."""


@unique
class Motor(IntEnum):
    """Roomba motor states."""

    OFF = 0
    """Turn motor off."""
    DEFAULT = 1
    """Turn motor on in its default direction."""
    OPPOSITE = 2
    """Turn motor on in its opposite direction (not available for the vacuum)."""


@unique
class Button(IntEnum):
    """Roomba buttons."""

    CLEAN = 0
    """The `CLEAN` button."""
    SPOT = 1
    """The `SPOT` button."""
    DOCK = 2
    """The `DOCK` button."""
    MINUTE = 3
    """The `MINUTE` button."""
    HOUR = 4
    """The `HOUR` button."""
    DAY = 5
    """The `DAY` button."""
    SCHEDULE = 6
    """The `SCHEDULE` button."""
    CLOCK = 7
    """The `CLOCK` button."""


class Roomba:
    """Roomba API for communicating with a physical Roomba vacuum cleaner through a serial connection."""

    _baud_codes = {
        300: BaudCode.B300,
        600: BaudCode.B600,
        1200: BaudCode.B1200,
        2400: BaudCode.B2400,
        4800: BaudCode.B4800,
        9600: BaudCode.B9600,
        14400: BaudCode.B14400,
        19200: BaudCode.B19200,
        28800: BaudCode.B28800,
        38400: BaudCode.B38400,
        57600: BaudCode.B57600,
        115200: BaudCode.B115200,
    }

    def __init__(self, serial: Serial, logger: Logger = None) -> Self:
        self.serial = serial
        self.logger = logger
        self._lock = Lock()

    def start(self) -> None:
        """Start the Open Interface (OI)."""
        data = bytes([Command.START])
        self.write(data)
        sleep(START_DURATION)  # The beep from the Roomba actually takes time...

    def set_baud_rate(self, baud_rate: int) -> None:
        """
        Set the baud rate.

        :param baud_rate: one of the twelve supported baud rates.
        :raises ValueError: if the specified `baud_rate` is not supported.
        """
        if baud_rate not in Roomba._baud_codes:
            raise ValueError(f"Baud rate {baud_rate} is usnupported by Roomba")
        self.set_baud(Roomba._baud_codes[baud_rate])

    def set_baud(self, baud_code: BaudCode) -> None:
        """
        Set the baud rate.

        :param baud_code: one of the twelve baud codes.
        """
        data = bytes([Command.BAUD, baud_code])
        self.write(data)
        sleep(MODE_CHANGE_DURATION)

    def control(self) -> None:
        """
        Enable control of the Roomba.

        Please note: the result of executing this command is to put the Roomba is Safe mode, so using `Roomba.safe()` is preferable.
        """
        data = bytes([Command.CONTROL])
        self.write(data)
        sleep(MODE_CHANGE_DURATION)

    def safe(self) -> None:
        """
        Put the OI into Safe mode, enabling control of the Roomba.

        The OI can be in Passive, Safe, or Full mode to accept this command. If a safety condition occurs Roomba reverts automatically to Passive mode.
        """
        data = bytes([Command.SAFE])
        self.write(data)
        sleep(MODE_CHANGE_DURATION)

    def full(self) -> None:
        """
        Put the OI into Full mode, enabling full control of the Roomba and turning off the cliff, wheel-drop and internal charger safety features.

        The OI can be in Passive, Safe, or Full mode to accept this command. In Full mode, Roomba executes any command that you send it, even if the internal
        charger is plugged in, or command triggers a cliff or wheel drop condition.
        """
        data = bytes([Command.FULL])
        self.write(data)
        sleep(MODE_CHANGE_DURATION)

    def power(self) -> None:
        """Power down the Roomba. The OI can be in Passive, Safe, or Full mode to accept this command."""
        data = bytes([Command.POWER])
        self.write(data)
        sleep(MODE_CHANGE_DURATION)

    def spot(self) -> None:
        """Start the Spot cleaning mode."""
        data = bytes([Command.SPOT])
        self.write(data)

    def clean(self) -> None:
        """Start the default cleaning mode."""
        data = bytes([Command.CLEAN])
        self.write(data)

    def max(self) -> None:
        """Start the Max cleaning mode."""
        data = bytes([Command.MAX])
        self.write(data)

    def drive(self, velocity: int, radius: int) -> None:
        """
        Instruct the Roomba to drive at the specified velocity (mm/s), turning at the specified radius (mm).

        :param velocity: the average velocity (-500 to 500 mm/s).
        :param radius: the radius of the turn (-2000 to 2000 mm).
            32767 or 32768 to drive straight
            -1 to turn clockwise in place
            1 to turn counter-clockwise in place
        :raises ValueError: if the `velocity` or the `radius` is invalid.
        """
        if velocity < -500 or velocity > 500:
            raise ValueError(f"Velocity {velocity} is unsupported by Roomba")
        if radius < -2000 or radius > 2000:
            raise ValueError(f"Radius {radius} is unsupported by Roomba")
        data = pack(">Bhh", Command.DRIVE, velocity, radius)
        self.write(data)

    def motors(self, main_brush: Motor, side_brush: Motor, vacuum: Motor) -> None:
        """
        Instruct the Roomba to turn its motors on and off.

        :param main_brush: the main brush motor setting (`Motor.OFF`, `Motor.DEFAULT`, or `Motor.OPPOSITE`).
        :param side_brush: the side brush motor setting (`Motor.OFF`, `Motor.DEFAULT`, or `Motor.OPPOSITE`).
        :param vacuum: the vacuum motor setting (`Motor.OFF` or `Motor.DEFAULT`).
        :raises ValueError` if `vacuum` is set to `Motor.OPPOSITE`.
        """
        motor_bits = 0b00000000
        if main_brush == Motor.OFF:
            pass
        elif main_brush == Motor.DEFAULT:
            motor_bits |= 0b00000100
        else:
            motor_bits |= 0b00010100
        if side_brush == Motor.OFF:
            pass
        elif side_brush == Motor.DEFAULT:
            motor_bits |= 0b00000001
        else:
            motor_bits |= 0b00001001
        if vacuum == Motor.OFF:
            pass
        elif vacuum == Motor.DEFAULT:
            motor_bits |= 0b00000010
        else:
            raise ValueError("Vacuum can only run in the default direction")
        data = bytes([Command.MOTORS, motor_bits])
        self.write(data)

    def leds(self, color: int, intensity: int, check_robot: bool, dock: bool, spot: bool, debris: bool) -> None:
        """
        Instruct the Roomba to turn its LEDs on and off.

        :param color: the color of the Clean/Power button (0 to 255).
        :param intensity: the intensity of the Clean/Power button (0 to 255).
        :param check_robot: `True` to turn the check robot LED on; `False` to turn it off.
        :param dock: `True` to turn the dock LED on; `False` to turn it off.
        :param spot: `True` to turn the spot LED on; `False` to turn it off.
        :param debris: `True` to turn the debris LED on; `False` to turn it off.
        :raises ValueError: if `color` or `intensity` is invalid.
        """
        if color < 0 or color > 255:
            raise ValueError(f"Color {color} is invalid")
        if intensity < 0 or intensity > 255:
            raise ValueError(f"Intensity {intensity} is invalid")
        led_bits = 0b00000000
        if check_robot is True:
            led_bits |= 0b00001000
        if dock is True:
            led_bits |= 0b00000100
        if spot is True:
            led_bits |= 0b00000010
        if debris is True:
            led_bits |= 0b00000001
        data = bytes([Command.LEDS, led_bits, color, intensity])
        self.write(data)

    def song(self, song: int, notes: List[Tuple[int, int]]) -> None:
        """
        Define a song the Roomba can play.

        :param song: the song (0 to 4).
        :param notes: `List` of tuples specifying note number (31 to 127) and duration (0 to 255) in 1/64th of a second.
        :raises ValueError: if `song` or `notes` is invalid.
        """
        if song < 0 or song > 4:
            raise ValueError(f"Song {song} is not supported by Roomba")
        if len(notes) == 0 or len(notes) > 16:
            raise ValueError(f"A song length of {len(notes)} notes is not supported by Roomba")
        for i in range(len(notes)):
            if notes[i][0] < 31 or notes[i][0] > 127:
                raise ValueError(f"Note number {notes[i][0]} at position {i} is not supported by Roomba")
            if notes[i][1] < 0 or notes[i][1] > 255:
                raise ValueError(f"Note duration {notes[i][1]} at position {i} is not supported by Roomba")
        a = [0] * (1 + 2 + 2 * len(notes))  # Command, song, number of notes, and two bytes per note
        a[0] = Command.SONG
        a[1] = song
        a[2] = len(notes)
        for i in range(len(notes)):
            a[3 + 2 * i] = notes[i][0]
            a[4 + 2 * i] = notes[i][1]
        data = bytes(a)
        self.write(data)

    def play(self, song: int) -> None:
        """
        Instruct the Roomba to play the specified song.

        :param song: the song (0 to 4).
        :raises ValueError: if `song` is invalid.
        """
        if song < 0 or song > 4:
            raise ValueError(f"Song {song} is not supported by Roomba")
        data = bytes([Command.PLAY, song])
        self.write(data)

    def sensors(self, id: int) -> Packet:
        """
        Request the sensors with the specified id to be queried.

        :param id: the id of the sensors to be queried.
        :returns: the requested sensor packet.
        :rtype: Packet.
        :raises ValueError: if `id` does not not a known `Packet` type.
        """
        if id not in Packet.registry:
            raise ValueError(f"Packet {id} is unknown")
        cls = Packet.registry[id]
        data = bytes([Command.SENSORS, id])
        data = self.write_and_read(data, size=cls.size)
        return cls.from_bytes(data)

    def seek_dock(self) -> None:
        """Instruct the Roomba to seek its dock."""
        data = bytes([Command.SEEK_DOCK])
        self.write(data)

    def motors_pwm(self, main_brush_pwm: int, side_brush_pwm: int, vacuum_pwm: int) -> None:
        """
        Instruct the Roomba to turn its motors on and off, using the specified, raw Pulse Width Modulation (PWM) values.

        :param main_brush_pwm: the main brush PWM (-127 to 127).
        :param side_brush_pwm: the side brush PWM (-127 to 127).
        :param vacuum_pwm: the vacuum PWM (0 to 127).
        :raises ValueError: if `main_brush_pwm`, `side_brush_pwm` or `vacuum_pwm` is invalid.
        """
        if main_brush_pwm < -127 or main_brush_pwm > 127:
            raise ValueError(f"Main brush PWM {main_brush_pwm} is invalid")
        if side_brush_pwm < -127 or side_brush_pwm > 127:
            raise ValueError(f"Side brush PWM {side_brush_pwm} is invalid")
        if vacuum_pwm < 0 or vacuum_pwm > 127:
            raise ValueError(f"Vacuum PWM {side_brush_pwm} is invalid")
        data = pack(">BbbB", Command.MOTORS_PWM, main_brush_pwm, side_brush_pwm, vacuum_pwm)
        self.write(data)

    def drive_direct(self, left_velocity: int, right_velocity: int) -> None:
        """
        Instruct the Roomba to drive at the specified left and right velocities.

        :param left_velocity: the left velocity (-500 to 500 mm/s).
        :param right_velocity: the right velocity (-500 to 500 mm/s).
        :raises ValueError: if `left_velocity` or `right_velocity` is invalid.

        Note: for readability, the method has the left velocity as the first, leftmost argument and the right velocity
        as the second, rightmost argument. When sending the command to the Roomba, the right velocity is the first short
        and the left velocity is the second short.
        """
        if left_velocity < -500 or left_velocity > 500:
            raise ValueError(f"Velocity {left_velocity} is unsupported by Roomba")
        if right_velocity < -500 or right_velocity > 500:
            raise ValueError(f"Velocity {right_velocity} is unsupported by Roomba")
        data = pack(">Bhh", Command.DRIVE_DIRECT, right_velocity, left_velocity)
        self.write(data)

    def drive_pwm(self, left_pwm: int, right_pwm: int) -> None:
        """
        Instruct the Roomba to drive using the specified, raw Pulse Width Modulation (PWM) values.

        :param left_pwm: the left PWM (-255 to 255)
        :param right_pwm: the right PWM (-255 to 255)
        :raises ValueError: if `left_pwm` or `right_pwm` is invalid.

        Note: for readability, the method has the left PWM as the first, leftmost argument and the right PWM
        as the second, rightmost argument. When sending the command to the Roomba, the right PWM is the first short
        and the left PWM is the second short.
        """
        if left_pwm < -255 or left_pwm > 255:
            raise ValueError(f"PWM {left_pwm} is unsupported by Roomba")
        if right_pwm < -255 or right_pwm > 255:
            raise ValueError(f"PWM {right_pwm} is unsupported by Roomba")
        data = pack(">Bhh", Command.DRIVE_PWM, right_pwm, left_pwm)
        self.write(data)

    def stream(self, ids: List[int]) -> int:
        """
        Instruct the Roomba to stream sensor packets every 15 ms.

        Please note:
        1. There is a theoretical max of 255 packets as the number of packets is sent as an unsigned byte.
        2. The maximum of amount of data is `(baudrate / 10) * (15 / 1000)`. For a baudrate of 57,600 that's 86 bytes and for 115,200 it's 172.

        :param ids: the `List` of packet ids.
        :returns: the raw size of the data that will be streamed from the Roomba.
        :rtype: int.
        :raises ValueError: if `ids` is invalid or the total length exceeds what is possible.
        """
        if len(ids) > 255:
            raise ValueError("Cannot request more than 255 packets")
        max_size = (self.serial.baudrate / 10) * (15 / 1000)  # 10 bits per byte; packets sent every 15 ms
        size = 0
        for id in ids:
            if id not in Packet.registry:
                raise ValueError(f"Packet id {id} is unknown")
            cls: Packet = Packet.registry[id]
            size += cls.size
        if size > max_size:
            raise ValueError(f"Too much data requested({size} - at {self.serial.baudrate} baud max size is {max_size}")
        a = [0] * (1 + 1 + len(ids))  # Command, number of packets, and 1 byte per packet id
        a[0] = Command.STREAM
        a[1] = len(ids)
        for i in range(len(ids)):
            a[2 + i] = ids[i]
        data = bytes(a)
        self.write(data)
        return 1 + 1 + len(ids) + size + 1  # Header, size, packet ids, size of packet data, and checksum

    def query_list(self, ids: List[int]) -> List[Packet]:
        """
        Instruct the Roomba to send a list of sensor packets.

        Please note: There is a theoretical max of 255 packets as the number of packets is sent as an unsigned byte.

        :param ids: the `List` of packet ids to query.
        :returns: the requested `List` of packets.
        :rtype: List[Packet].
        :raises ValueError: if `ids` is invalid.
        """
        if len(ids) > 255:
            raise ValueError("Cannot request more than 255 packets")
        size = 0
        for id in ids:
            if id not in Packet.registry:
                raise ValueError(f"Packet id {id} is unknown")
            cls: Packet = Packet.registry[id]
            size += cls.size
        a = [0] * (1 + 1 + len(ids))  # Command, number of packets, and 1 byte per packet id
        a[0] = Command.QUERY_LIST
        a[1] = len(ids)
        for i in range(len(ids)):
            a[2 + i] = ids[i]
        data = bytes(a)
        data = self.write_and_read(data, size=size)
        packets = []
        offset = 0
        for id in ids:
            cls: Packet = Packet.registry[id]
            packet = cls.from_bytes(data, offset=offset)
            packets.append(packet)
            offset += cls.size
        return packets

    def pause_resume_stream(self, start: bool) -> None:
        """
        Instruct the Roomba to pause or resume the stream of packets requested with `Roomba.stream()`.

        :param start: `True` to start streaming packets; `False` otherwise.
        """
        data = bytes([Command.PAUSE_RESUME_STREAM, int(start)])
        self.write(data)

    def digit_leds_ascii(self, digits: str) -> None:
        """
        Instruct the Roomba to turn on the LEDs to display ASCII characters.

        :param digits: The four (4) digits.
        """
        if len(digits) != 4:
            raise ValueError(f"Digits '{digits}' not valid - must be 4 characters")
        for c in digits:
            value = ord(c)
            if value < 32 or value > 126:
                raise ValueError(f"Digit {value} not valid - must be 32 to 126")
        data = bytes([Command.DIGIT_LEDS_ASCII]) + bytes(digits, "ASCII")
        self.write(data)

    def buttons(self, buttons: List[Button]) -> None:
        """
        Instruct the Roomba to "press" one or more of its buttons.

        :param buttons: `List` of buttons to press.
        """
        button_bits = 0b00000000
        for button in buttons:
            button_bits |= 1 << button
        data = bytes([Command.BUTTONS, button_bits])
        self.write(data)

    def button(self, button: Button) -> None:
        """
        Instruct the Roomba to "press" the specified button.

        :param button: the button to press
        """
        self.buttons([button])

    def set_date_time(self, date_time: datetime) -> None:
        """
        Set the Roomba's day/time.

        :param date_time: the date/time to set the day/time from
        """
        iso_week_day = date_time.isoweekday()
        if iso_week_day == 7:
            iso_week_day = 0
        week_day = WeekDay(iso_week_day)
        self.set_day_time(week_day, date_time.hour, date_time.minute)

    def set_day_time(self, week_day: WeekDay, hour: int, minute: int) -> None:
        """
        Set the Roomba's day/time.

        :param week_day: the week day.
        :param hour: the hour (0 to 23).
        :param minute: the minute (0 to 59).
        :raises ValueError: if `hour` or `minute` is invalid.
        """
        if hour < 0 or hour > 23:
            raise ValueError(f"Hour {hour} is invalid")
        if minute < 0 or minute > 59:
            raise ValueError(f"Minute {minute} is invalid")
        data = bytes([Command.SET_DAY_TIME, int(week_day), hour, minute])
        self.write(data)

    def write(self, data: bytes):
        """
        Write the specified data to the Roomba via the serial port.

        :param data: the raw bytes of data to send to the Roomba.
        """
        self._dump_data("Writing data:", data)
        self._lock.acquire()
        try:
            self.serial.write(data)
            self.serial.flush()
        finally:
            self._lock.release()
        sleep(COMMAND_PROCESS_DURATION)

    def read(self, size: int = 1) -> bytes:
        """
        Read data of the specified size from the Roomba via the serial port.

        :param size: the size of the data to read (in number of bytes)
        :returns: the requested data.
        """
        self._lock.acquire()
        try:
            data = self.serial.read(size=size)
            self._dump_data("Read data:", data)
            return data
        finally:
            self._lock.release()

    def write_and_read(self, data: bytes, size: int = 1) -> bytes:
        """
        Write the specified data to the Roomba and read data of the specified size from the Roomba via the serial port.


        :param data: the raw bytes of data to send to the Roomba.
        :param size: the size of the data to read (in number of bytes).
        :returns: the requested data.
        :rtype: bytes.
        """
        self._lock.acquire()
        try:
            self._dump_data("Writing data:", data)
            self.serial.write(data)
            self.serial.flush()
            sleep(COMMAND_PROCESS_DURATION)
            data = self.serial.read(size=size)
            self._dump_data("Read data:", data)
            return data
        finally:
            self._lock.release()

    def _dump_data(self, message: str, data: bytes) -> None:
        """
        Dump data being sent or received.

        :param message: the message to output before the hex dump.
        :param data: the data.
        """
        if self.logger is None or not self.logger.isEnabledFor(DEBUG):
            return
        io = StringIO()
        hex_dump(data, io)
        self.logger.debug(message)
        for line in io.getvalue().split("\n"):
            if len(line) > 0:
                self.logger.debug(line)
