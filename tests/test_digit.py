import unittest
from unittest.mock import MagicMock, patch
from machine import Pin, PWM, RTC
from digit.digit import Digit, Motoractuator

class TestMotoractuator(unittest.TestCase):
    @patch('machine.PWM')
    @patch('machine.Pin')
    def test_extend(self, mock_pin, mock_pwm):
        mock_pwm_instance = mock_pwm.return_value
        actuator = Motoractuator(11, 12, 13)
        actuator.extend(50, 0.1)
        mock_pwm_instance.duty_u16.assert_called_with(int((50 / 100) * 65536))
        mock_pin.return_value.on.assert_called_once()

    @patch('machine.PWM')
    @patch('machine.Pin')
    def test_retract(self, mock_pin, mock_pwm):
        mock_pwm_instance = mock_pwm.return_value
        actuator = Motoractuator(11, 12, 13)
        actuator.retract(50, 0.1)
        mock_pwm_instance.duty_u16.assert_called_with(int((50 / 100) * 65536))
        mock_pin.return_value.on.assert_called_once()

class TestDigit(unittest.TestCase):
    @patch('machine.RTC')
    @patch('machine.PWM')
    @patch('machine.Pin')
    @patch('common.config.Config')
    def setUp(self, mock_config, mock_pin, mock_pwm, mock_rtc):
        self.mock_config = mock_config.return_value
        self.mock_config.read.side_effect = lambda key, default=None: default
        self.digit = Digit([2, 3, 6, 7, 8, 9, 28], 0.5, [(12, 13), (14, 15), (16, 17), (18, 19), (20, 21), (22, 26), (27, 10)])

    def test_load_config(self):
        self.mock_config.read.assert_any_call("previous", default=[0] * 7)
        self.mock_config.read.assert_any_call("brightness", default=0.5)
        self.mock_config.read.assert_any_call("motorspeed", default=50)
        self.mock_config.read.assert_any_call("waitTime", default=0.02)

    @patch('time.sleep', return_value=None)
    def test_extend_segment(self, mock_sleep):
        self.digit.extend_segment(0)
        self.assertEqual(self.digit.previous_digit_array[0], 1)

    @patch('time.sleep', return_value=None)
    def test_retract_segment(self, mock_sleep):
        self.digit.previous_digit_array[0] = 1
        self.digit.retract_segment(0)
        self.assertEqual(self.digit.previous_digit_array[0], 0)

    @patch('time.sleep', return_value=None)
    def test_set_digit(self, mock_sleep):
        digit_array = [1, 0, 1, 0, 1, 0, 1]
        moves = self.digit.set_digit(digit_array)
        self.assertEqual(moves, 7)
        self.assertEqual(self.digit.previous_digit_array, digit_array)

    @patch('time.sleep', return_value=None)
    def test_dance(self, mock_sleep):
        moves = self.digit.dance()
        self.assertEqual(moves, 14)

    @patch('time.sleep', return_value=None)
    def test_set_time_display(self, mock_sleep):
        self.digit.rtc.datetime.return_value = (2000, 1, 1, 0, 12, 34, 56, 0)
        self.digit.setTimeDisplay(twelveHour=False)
        self.assertEqual(self.digit.previous_digit_array, [0, 0, 1, 1, 0, 0, 0])

if __name__ == '__main__':
    unittest.main()
