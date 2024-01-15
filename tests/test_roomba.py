"""
Tests for Roomba.
"""


from datetime import datetime
from typing import List, Optional
from unittest.mock import MagicMock

from pytest import raises
from serial import Serial

from irobot.packet import Mode, Packet, Packet7, Packet15, Packet35
from irobot.roomba import BaudCode, Button, Motor, Roomba, WeekDay


def create_mocked_roomba(return_value: Optional[bytes] = None) -> Roomba:
    """Creates a mocked `Roomba`.

    Parameters
    ----------
    return_value : Optional[bytes], optional
        The mocked return value, by default None

    Returns
    -------
    Roomba
        The `Roomba`.
    """
    serial = Serial()
    serial.baudrate = 115200
    serial.write = MagicMock()
    serial.flush = MagicMock()
    if return_value is not None:
        serial.read = MagicMock(return_value=return_value)
    roomba = Roomba(serial)
    return roomba


def test_start():
    """Tests start."""
    roomba = create_mocked_roomba()
    roomba.start()
    roomba.serial.write.assert_called_once_with(bytes([128]))


def test_set_baud_rate():
    """Tests set baud rate."""
    roomba = create_mocked_roomba()
    roomba.set_baud_rate(57600)
    roomba.serial.write.assert_called_once_with(bytes([129, 10]))


def test_set_baud_rate_invalid_baud_rate():
    """Tests set baud rate with an invalid value."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.set_baud_rate(12345)


def test_set_baud():
    """Tests set baud."""
    roomba = create_mocked_roomba()
    roomba.set_baud(BaudCode.B57600)
    roomba.serial.write.assert_called_once_with(bytes([129, 10]))


def test_control():
    """Tests control."""
    roomba = create_mocked_roomba()
    roomba.control()
    roomba.serial.write.assert_called_once_with(bytes([130]))


def test_safe():
    """Tests safe."""
    roomba = create_mocked_roomba()
    roomba.safe()
    roomba.serial.write.assert_called_once_with(bytes([131]))


def test_full():
    """Tests full."""
    roomba = create_mocked_roomba()
    roomba.full()
    roomba.serial.write.assert_called_once_with(bytes([132]))


def test_power():
    """Tests power."""
    roomba = create_mocked_roomba()
    roomba.power()
    roomba.serial.write.assert_called_once_with(bytes([133]))


def test_spot():
    """Tests spot."""
    roomba = create_mocked_roomba()
    roomba.spot()
    roomba.serial.write.assert_called_once_with(bytes([134]))


def test_clean():
    """Tests clean."""
    roomba = create_mocked_roomba()
    roomba.clean()
    roomba.serial.write.assert_called_once_with(bytes([135]))


def test_max():
    """Tests max."""
    roomba = create_mocked_roomba()
    roomba.max()
    roomba.serial.write.assert_called_once_with(bytes([136]))


def test_drive():
    """Tests drive."""
    roomba = create_mocked_roomba()
    roomba.drive(-200, 500)
    roomba.serial.write.assert_called_once_with(bytes([137, 255, 56, 1, 244]))


def test_drive_invalid_velocity():
    """Tests drive with invalid velocity."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive(5000, 500)


def test_drive_invalid_radius():
    """Tests drive with invalid radius."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive(-200, 5000)


def test_motors():
    """Tests motors."""
    roomba = create_mocked_roomba()
    roomba.motors(Motor.DEFAULT, Motor.DEFAULT, Motor.DEFAULT)
    roomba.serial.write.assert_called_once_with(bytes([138, 0b00000111]))


def test_motors_opposite():
    """Tests motors with opposite."""
    roomba = create_mocked_roomba()
    roomba.motors(Motor.OPPOSITE, Motor.OPPOSITE, Motor.DEFAULT)
    roomba.serial.write.assert_called_once_with(bytes([138, 0b00011111]))


def test_motors_off():
    """Tests motors off."""
    roomba = create_mocked_roomba()
    roomba.motors(Motor.OFF, Motor.OFF, Motor.OFF)
    roomba.serial.write.assert_called_once_with(bytes([138, 0b00000000]))


def test_motors_invalid_vacuum():
    """Tests motors invalid vacuum direction."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.motors(Motor.DEFAULT, Motor.DEFAULT, Motor.OPPOSITE)


def test_leds():
    """Tests LEDs."""
    roomba = create_mocked_roomba()
    roomba.leds(100, 200, False, True, False, False)
    roomba.serial.write.assert_called_once_with(bytes([139, 0b00000100, 100, 200]))


def test_leds_all_on():
    """Tests LEDs all on."""
    roomba = create_mocked_roomba()
    roomba.leds(255, 255, True, True, True, True)
    roomba.serial.write.assert_called_once_with(bytes([139, 0b00001111, 255, 255]))


def test_leds_all_off():
    """Tests LEDs all off."""
    roomba = create_mocked_roomba()
    roomba.leds(0, 0, False, False, False, False)
    roomba.serial.write.assert_called_once_with(bytes([139, 0b00000000, 0, 0]))


def test_leds_invalid_color():
    """Tests LEDs all invalid color."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.leds(256, 200, False, False, False, False)


def test_leds_invalid_intensity():
    """Tests LEDs all invalid intensity."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.leds(100, -1, False, False, False, False)


def test_song():
    """Tests song."""
    roomba = create_mocked_roomba()
    roomba.song(0, [(31, 4), (32, 8), (100, 16)])
    roomba.serial.write.assert_called_once_with(bytes([140, 0, 3, 31, 4, 32, 8, 100, 16]))


def test_song_invalid_song():
    """Tests song with invalid song."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.song(5, [(31, 4), (32, 8), (100, 16)])


def test_song_invalid_song_length():
    """Tests song with invalid song length."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.song(2, [])


def test_song_invalid_note_number():
    """Tests song with invalid note number."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.song(0, [(31, 4), (200, 8), (100, 16)])


def test_song_invalid_note_duration():
    """Tests song with invalid note length."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.song(0, [(31, 4), (32, 500), (100, 16)])


def test_play():
    """Tests play."""
    roomba = create_mocked_roomba()
    roomba.play(1)
    roomba.serial.write.assert_called_once_with(bytes([141, 1]))


def test_play_invalid_song():
    """Tests play with invalid song."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.play(5)


def test_sensors():
    """Tests sensors."""
    roomba = create_mocked_roomba(return_value=bytes([0b00001111]))
    packet = roomba.sensors(7)
    assert packet is not None
    assert type(packet) == Packet7
    assert packet.wheel_drop_left is True
    assert packet.wheel_drop_right is True
    assert packet.bump_left is True
    assert packet.bump_right is True


def test_sensors_invalid_id():
    """Tests sensors with invalid id."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.sensors(1000)


def test_seek_dock():
    """Tests seek dock."""
    roomba = create_mocked_roomba()
    roomba.seek_dock()
    roomba.serial.write.assert_called_once_with(bytes([143]))


def test_motors_pwm():
    """Tests motors using PWM."""
    roomba = create_mocked_roomba()
    roomba.motors_pwm(100, -50, 25)
    roomba.serial.write.assert_called_once_with(bytes([144, 100, 206, 25]))


def test_motors_pwm_invalid_main_brush():
    """Tests motors using PWM with invalid main brush."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.motors_pwm(200, -50, 25)


def test_motors_pwm_invalid_side_brush():
    """Tests motors using PWM with invalid side brush."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.motors_pwm(100, -150, 25)


def test_motors_pwm_invalid_vacuum():
    """Tests motors using PWM with invalid vacuum."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.motors_pwm(100, -50, -25)


def test_drive_direct():
    """Tests drive direct."""
    roomba = create_mocked_roomba()
    roomba.drive_direct(300, 150)
    roomba.serial.write.assert_called_once_with(bytes([145, 0, 150, 1, 44]))


def test_drive_direct_invalid_left_velocity():
    """Tests drive direct with invalid left velocity."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive_direct(300, 999)


def test_drive_direct_invalid_right_velocity():
    """Tests drive direct with invalid right velocity."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive_direct(999, 300)


def test_drive_pwm():
    """Tests drive using PWM."""
    roomba = create_mocked_roomba()
    roomba.drive_pwm(-100, 100)
    roomba.serial.write.assert_called_once_with(bytes([146, 0, 100, 255, 156]))


def test_drive_pwm_invalid_left_pwm():
    """Tests drive using PWM with invalid left value."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive_pwm(-1000, 100)


def test_drive_pwm_invalid_right_pwm():
    """Tests drive using PWM with invalid right value."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive_pwm(-100, 1000)


def test_stream():
    """Tests stream."""
    roomba = create_mocked_roomba()
    size = roomba.stream([29, 13])
    roomba.serial.write.assert_called_once_with(bytes([148, 2, 29, 13]))
    assert size == 8


def test_stream_too_many_packets():
    """Tests stream with too many packets."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.stream([0] * 256)


def test_stream_invalid_packet_id():
    """Tests stream with invalid packet id."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.stream([7, 200, 35])


def test_stream_too_much_data():
    """Tests stream with too much data."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.stream([6, 6, 6, 6])


def test_query_list():
    """Tests query list."""
    roomba = create_mocked_roomba(return_value=bytes([2, 42]))
    packets: List[Packet] = roomba.query_list([35, 15])
    roomba.serial.write.assert_called_once_with(bytes([149, 2, 35, 15]))
    assert packets is not None
    assert len(packets) == 2
    assert type(packets[0]) == Packet35
    assert type(packets[1]) == Packet15
    packet_35: Packet35 = packets[0]
    assert packet_35.mode == Mode.SAFE
    packet_15: Packet15 = packets[1]
    assert packet_15.dirt_detect == 42


def test_query_list_too_many_packets():
    """Tests query list with too many packets."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.query_list([0] * 256)


def test_query_list_invalid_packet_id():
    """Tests query list with invalid packet id."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.query_list([7, 200, 35])


def test_pause_resume_stream_start():
    """Tests pause/resume start."""
    roomba = create_mocked_roomba()
    roomba.pause_resume_stream(True)
    roomba.serial.write.assert_called_once_with(bytes([150, 1]))


def test_pause_resume_stream_stop():
    """Tests pause/resume stop."""
    roomba = create_mocked_roomba()
    roomba.pause_resume_stream(False)
    roomba.serial.write.assert_called_once_with(bytes([150, 0]))


def test_leds_ascii():
    """Tests ASCII LEDs."""
    roomba = create_mocked_roomba()
    roomba.digit_leds_ascii("RMBA")
    roomba.serial.write.assert_called_once_with(bytes([164, 82, 77, 66, 65]))


def test_leds_ascii_wrong_length():
    """Tests ASCII LEDs with wrong length."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.digit_leds_ascii("ROOMBA")


def test_leds_ascii_invalid_character():
    """Tests ASCII LEDs with invalid character."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.digit_leds_ascii("RMB\t")


def test_buttons():
    """Tests buttons."""
    roomba = create_mocked_roomba()
    roomba.buttons([Button.CLOCK, Button.SCHEDULE])
    roomba.serial.write.assert_called_once_with(bytes([165, 0b11000000]))


def test_button():
    """Tests button."""
    roomba = create_mocked_roomba()
    roomba.button(Button.DOCK)
    roomba.serial.write.assert_called_once_with(bytes([165, 0b00000100]))


def test_set_date_time():
    """Tests set date time."""
    date_time = datetime.fromisoformat("2022-04-24T07:27:21.966346")
    roomba = create_mocked_roomba()
    roomba.set_date_time(date_time)
    roomba.serial.write.assert_called_once_with(bytes([168, 0, 7, 27]))


def test_set_day_time():
    """Tests set day time."""
    roomba = create_mocked_roomba()
    roomba.set_day_time(WeekDay.MONDAY, 11, 22)
    roomba.serial.write.assert_called_once_with(bytes([168, 1, 11, 22]))


def test_set_day_time_invalid_hour():
    """Tests set day time with invalid hour."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.set_day_time(WeekDay.MONDAY, 24, 22)


def test_set_day_time_invalid_minute():
    """Tests set day time with invalid minute."""
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.set_day_time(WeekDay.MONDAY, 11, -3)


def test_write():
    """Tests write."""
    roomba = create_mocked_roomba()
    roomba.write(bytes([1, 2, 3, 4]))
    roomba.serial.write.assert_called_once_with(bytes([1, 2, 3, 4]))


def test_read():
    """Tests read."""
    roomba = create_mocked_roomba(return_value=bytes([4, 3, 2, 1]))
    data = roomba.read(size=4)
    roomba.serial.read.assert_called_once_with(size=4)
    assert data == bytes([4, 3, 2, 1])


def test_write_and_read():
    """Tests write and read."""
    roomba = create_mocked_roomba(return_value=bytes([4, 3, 2, 1]))
    data = roomba.write_and_read(bytes([1, 2, 3, 4]), size=4)
    roomba.serial.write.assert_called_once_with(bytes([1, 2, 3, 4]))
    roomba.serial.read.assert_called_once_with(size=4)
    assert data == bytes([4, 3, 2, 1])
