""" SWTP_Ebner_WiSe23_Getraenkemaschine
Tests for SerialMessage classes

Version 0.1
Licence: MIT
"""

import unittest

from parser.serial_message import SerialMessage

class TestSerial(unittest.TestCase):
    def test_info(self):
        input = 'info,1'

        serial_message = SerialMessage.create(input)
        self.assertTrue(serial_message.is_valid())

        output = serial_message.to_json()
        self.assertEqual(output, '{"type": "info", "value": 1}')

    def test_invalid_info(self):
        input = 'info,1,2'

        serial_message = SerialMessage.create(input)
        self.assertFalse(serial_message.is_valid())

        input = 'info,ok'

        serial_message = SerialMessage.create(input)
        self.assertFalse(serial_message.is_valid())

    def test_error(self):
        input = 'error,0,1'

        serial_message = SerialMessage.create(input)
        self.assertTrue(serial_message.is_valid())

        output = serial_message.to_json()
        self.assertEqual(output, '{"type": "error", "value": {"error_code": 0, "error_info": 1}}')

    def test_invalid_error(self):
        input = 'error,0'

        serial_message = SerialMessage.create(input)
        self.assertFalse(serial_message.is_valid())

        input = 'error,0,glass removed'

        serial_message = SerialMessage.create(input)
        self.assertFalse(serial_message.is_valid())

    def test_unknown(self):
        input = 'message,1'

        serial_message = SerialMessage.create(input)
        self.assertFalse(serial_message.is_valid())

if __name__ == '__main__':
    unittest.main()