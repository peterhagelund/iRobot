"""
Tests for Roomba.
"""


from datetime import datetime
from typing import List
from unittest.mock import MagicMock

from irobot.packet import Mode, Packet, Packet7, Packet15, Packet35
from irobot.roomba import BaudCode, Button, Motor, Roomba, WeekDay
from pytest import raises
from serial import Serial


def create_mocked_roomba(return_value: bytes = None) -> Roomba:
    serial = Serial()
    serial.baudrate = 115200
    serial.write = MagicMock()
    serial.flush = MagicMock()
    if return_value is not None:
        serial.read = MagicMock(return_value=return_value)
    roomba = Roomba(serial)
    return roomba


def test_start():
    roomba = create_mocked_roomba()
    roomba.start()
    roomba.serial.write.assert_called_once_with(bytes([128]))


def test_set_baud_rate():
    roomba = create_mocked_roomba()
    roomba.set_baud_rate(57600)
    roomba.serial.write.assert_called_once_with(bytes([129, 10]))


def test_set_baud_rate_invalid_baud_rate():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.set_baud_rate(12345)


def test_set_baud():
    roomba = create_mocked_roomba()
    roomba.set_baud(BaudCode.B57600)
    roomba.serial.write.assert_called_once_with(bytes([129, 10]))


def test_control():
    roomba = create_mocked_roomba()
    roomba.control()
    roomba.serial.write.assert_called_once_with(bytes([130]))


def test_safe():
    roomba = create_mocked_roomba()
    roomba.safe()
    roomba.serial.write.assert_called_once_with(bytes([131]))


def test_full():
    roomba = create_mocked_roomba()
    roomba.full()
    roomba.serial.write.assert_called_once_with(bytes([132]))


def test_power():
    roomba = create_mocked_roomba()
    roomba.power()
    roomba.serial.write.assert_called_once_with(bytes([133]))


def test_spot():
    roomba = create_mocked_roomba()
    roomba.spot()
    roomba.serial.write.assert_called_once_with(bytes([134]))


def test_clean():
    roomba = create_mocked_roomba()
    roomba.clean()
    roomba.serial.write.assert_called_once_with(bytes([135]))


def test_max():
    roomba = create_mocked_roomba()
    roomba.max()
    roomba.serial.write.assert_called_once_with(bytes([136]))


def test_drive():
    roomba = create_mocked_roomba()
    roomba.drive(-200, 500)
    roomba.serial.write.assert_called_once_with(bytes([137, 255, 56, 1, 244]))


def test_drive_invalid_velocity():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive(5000, 500)


def test_drive_invalid_radius():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive(-200, 5000)


def test_motors():
    roomba = create_mocked_roomba()
    roomba.motors(Motor.DEFAULT, Motor.DEFAULT, Motor.DEFAULT)
    roomba.serial.write.assert_called_once_with(bytes([138, 0b00000111]))


def test_motors_opposite():
    roomba = create_mocked_roomba()
    roomba.motors(Motor.OPPOSITE, Motor.OPPOSITE, Motor.DEFAULT)
    roomba.serial.write.assert_called_once_with(bytes([138, 0b00011111]))


def test_motors_off():
    roomba = create_mocked_roomba()
    roomba.motors(Motor.OFF, Motor.OFF, Motor.OFF)
    roomba.serial.write.assert_called_once_with(bytes([138, 0b00000000]))


def test_motors_invalid_vacuum():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.motors(Motor.DEFAULT, Motor.DEFAULT, Motor.OPPOSITE)


def test_leds():
    roomba = create_mocked_roomba()
    roomba.leds(100, 200, False, True, False, False)
    roomba.serial.write.assert_called_once_with(bytes([139, 0b00000100, 100, 200]))


def test_leds_all_on():
    roomba = create_mocked_roomba()
    roomba.leds(255, 255, True, True, True, True)
    roomba.serial.write.assert_called_once_with(bytes([139, 0b00001111, 255, 255]))


def test_leds_all_off():
    roomba = create_mocked_roomba()
    roomba.leds(0, 0, False, False, False, False)
    roomba.serial.write.assert_called_once_with(bytes([139, 0b00000000, 0, 0]))


def test_leds_invalid_color():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.leds(256, 200, False, False, False, False)


def test_leds_invalid_intensity():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.leds(100, -1, False, False, False, False)


def test_song():
    roomba = create_mocked_roomba()
    roomba.song(0, [(31, 4), (32, 8), (100, 16)])
    roomba.serial.write.assert_called_once_with(bytes([140, 0, 3, 31, 4, 32, 8, 100, 16]))


def test_song_invalid_song():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.song(5, [(31, 4), (32, 8), (100, 16)])


def test_song_invalid_song_length():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.song(2, [])


def test_song_invalid_note_number():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.song(0, [(31, 4), (200, 8), (100, 16)])


def test_song_invalid_note_duration():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.song(0, [(31, 4), (32, 500), (100, 16)])


def test_play():
    roomba = create_mocked_roomba()
    roomba.play(1)
    roomba.serial.write.assert_called_once_with(bytes([141, 1]))


def test_play_invalid_song():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.play(5)


def test_sensors():
    roomba = create_mocked_roomba(return_value=bytes([0b00001111]))
    packet = roomba.sensors(7)
    assert packet is not None
    assert type(packet) == Packet7
    assert packet.wheel_drop_left is True
    assert packet.wheel_drop_right is True
    assert packet.bump_left is True
    assert packet.bump_right is True


def test_sensors_invalid_id():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.sensors(1000)


def test_seek_dock():
    roomba = create_mocked_roomba()
    roomba.seek_dock()
    roomba.serial.write.assert_called_once_with(bytes([143]))


def test_motors_pwm():
    roomba = create_mocked_roomba()
    roomba.motors_pwm(100, -50, 25)
    roomba.serial.write.assert_called_once_with(bytes([144, 100, 206, 25]))


def test_motors_pwm_invalid_main_brush():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.motors_pwm(200, -50, 25)


def test_motors_pwm_invalid_side_brush():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.motors_pwm(100, -150, 25)


def test_motors_pwm_invalid_vacuum():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.motors_pwm(100, -50, -25)


def test_drive_direct():
    roomba = create_mocked_roomba()
    roomba.drive_direct(300, 150)
    roomba.serial.write.assert_called_once_with(bytes([145, 0, 150, 1, 44]))


def test_drive_direct_invalid_left_velocity():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive_direct(300, 999)


def test_drive_direct_invalid_right_velocity():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive_direct(999, 300)


def test_drive_pwm():
    roomba = create_mocked_roomba()
    roomba.drive_pwm(-100, 100)
    roomba.serial.write.assert_called_once_with(bytes([146, 0, 100, 255, 156]))


def test_drive_pwm_invalid_left_pwm():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive_pwm(-1000, 100)


def test_drive_pwm_invalid_right_pwm():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.drive_pwm(-100, 1000)


def test_stream():
    roomba = create_mocked_roomba()
    size = roomba.stream([29, 13])
    roomba.serial.write.assert_called_once_with(bytes([148, 2, 29, 13]))
    assert size == 8


def test_stream_too_many_packets():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.stream([0] * 256)


def test_stream_invalid_packet_id():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.stream([7, 200, 35])


def test_stream_too_much_data():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.stream([6, 6, 6, 6])


def test_query_list():
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
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.query_list([0] * 256)


def test_query_list_invalid_packet_id():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.query_list([7, 200, 35])


def test_pause_resume_stream_start():
    roomba = create_mocked_roomba()
    roomba.pause_resume_stream(True)
    roomba.serial.write.assert_called_once_with(bytes([150, 1]))


def test_pause_resume_stream_stop():
    roomba = create_mocked_roomba()
    roomba.pause_resume_stream(False)
    roomba.serial.write.assert_called_once_with(bytes([150, 0]))


def test_leds_ascii():
    roomba = create_mocked_roomba()
    roomba.digit_leds_ascii("RMBA")
    roomba.serial.write.assert_called_once_with(bytes([164, 82, 77, 66, 65]))


def test_leds_ascii_wrong_length():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.digit_leds_ascii("ROOMBA")


def test_leds_ascii_invalid_character():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.digit_leds_ascii("RMB\t")


def test_buttons():
    roomba = create_mocked_roomba()
    roomba.buttons([Button.CLOCK, Button.SCHEDULE])
    roomba.serial.write.assert_called_once_with(bytes([165, 0b11000000]))


def test_button():
    roomba = create_mocked_roomba()
    roomba.button(Button.DOCK)
    roomba.serial.write.assert_called_once_with(bytes([165, 0b00000100]))


def test_set_date_time():
    date_time = datetime.fromisoformat("2022-04-24T07:27:21.966346")
    roomba = create_mocked_roomba()
    roomba.set_date_time(date_time)
    roomba.serial.write.assert_called_once_with(bytes([168, 0, 7, 27]))


def test_set_day_time():
    roomba = create_mocked_roomba()
    roomba.set_day_time(WeekDay.MONDAY, 11, 22)
    roomba.serial.write.assert_called_once_with(bytes([168, 1, 11, 22]))


def test_set_day_time_invalid_hour():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.set_day_time(WeekDay.MONDAY, 24, 22)


def test_set_day_time_invalid_minute():
    roomba = create_mocked_roomba()
    with raises(ValueError):
        roomba.set_day_time(WeekDay.MONDAY, 11, -3)


def test_write():
    roomba = create_mocked_roomba()
    roomba.write(bytes([1, 2, 3, 4]))
    roomba.serial.write.assert_called_once_with(bytes([1, 2, 3, 4]))


def test_read():
    roomba = create_mocked_roomba(return_value=bytes([4, 3, 2, 1]))
    data = roomba.read(size=4)
    roomba.serial.read.assert_called_once_with(size=4)
    assert data == bytes([4, 3, 2, 1])


def test_write_and_read():
    roomba = create_mocked_roomba(return_value=bytes([4, 3, 2, 1]))
    data = roomba.write_and_read(bytes([1, 2, 3, 4]), size=4)
    roomba.serial.write.assert_called_once_with(bytes([1, 2, 3, 4]))
    roomba.serial.read.assert_called_once_with(size=4)
    assert data == bytes([4, 3, 2, 1])
