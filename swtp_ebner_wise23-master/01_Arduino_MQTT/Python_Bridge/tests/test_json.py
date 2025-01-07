""" SWTP_Ebner_WiSe23_Getraenkemaschine
Tests for JSONMessage classes

Version 0.1
Licence: MIT
"""

import unittest

from parser.json_message import JSONMessage

class TestJSON(unittest.TestCase):
    def test_config(self):
        input = '{ "type": "config", "value": [ { "configID": 1, "stationID": 0, "position": 30, "pump_pin": 3, "led_pin": 20 } ] }'

        json_message = JSONMessage.create(input)
        self.assertTrue(json_message.is_valid())

        output = json_message.to_serial()
        self.assertEqual(output, ['config,1,0,30,3,20'])

    def test_multiple_configs(self):
        input = '{ "type": "config", "value": [ { "configID": 0, "stationID": 0, "position": 31, "pump_pin": 4, "led_pin": 33 }, { "configID": 0, "stationID": 1, "position": 60, "pump_pin": 8, "led_pin": 36 } ] }'

        json_message = JSONMessage.create(input)
        self.assertTrue(json_message.is_valid())

        output = json_message.to_serial()
        self.assertEqual(output, ['config,0,0,31,4,33', 'config,0,1,60,8,36'])

    def test_invalid_config(self):
        input = '{ "type": "config", "value": [ { "stationType": 1, "stationID": 0, "position": 30, "pump_pin": 3, "led_pin": 20 } ] }'

        json_message = JSONMessage.create(input)
        self.assertFalse(json_message.is_valid())

        input = '{ "type": "config" }'

        json_message = JSONMessage.create(input)
        self.assertFalse(json_message.is_valid())

    def test_order(self):
        input = '{ "type": "order", "glass_weight": 236, "value": [ { "stationID": 0, "value": 25}, { "stationID": 2, "value": 50 } ] }'

        json_message = JSONMessage.create(input)
        self.assertTrue(json_message.is_valid())

        output = json_message.to_serial()
        self.assertEqual(output, ['order,2,236,0,25,2,50'])

    def test_invalid_order(self):
        input = '{ "type": "order", "glass_weight": 236, "value": [ { "stationID": 0}, { "stationID": 2, "value": 50 } ] }'

        json_message = JSONMessage.create(input)
        self.assertFalse(json_message.is_valid())

        input = '{ "type": "order", "glass_weight": 236, "value": [] }'

        json_message = JSONMessage.create(input)
        self.assertFalse(json_message.is_valid())

    def test_led(self):
        input = '{ "type": "led", "value": [ { "stationID": 0, "colorID": 1 } ] }'

        json_message = JSONMessage.create(input)
        self.assertTrue(json_message.is_valid())

        output = json_message.to_serial()
        self.assertEqual(output, ['led,0,1'])

    def test_multiple_leds(self):
        input = '{ "type": "led", "value": [ { "stationID": 0, "colorID": 1 }, { "stationID": 1, "colorID": 0 } ] }'

        json_message = JSONMessage.create(input)
        self.assertTrue(json_message.is_valid())

        output = json_message.to_serial()
        self.assertEqual(output, ['led,0,1', 'led,1,0'])

    def test_invalid_led(self):
        input =  '{ "type": "led", "value": [ { "stationID": 0, "colorID": 1 }, { "colorID": 0 } ] }'

        json_message = JSONMessage.create(input)
        self.assertFalse(json_message.is_valid())

        input = '{ "type": "led", "value": [ { "stationID": -1, "colorID": 10 } ] }'

        json_message = JSONMessage.create(input)
        self.assertFalse(json_message.is_valid())

    def test_unknown(self):
        input = '{ "type": "createorder", "glass_weight": 236, "value": [ { "stationID": 0, "value": 25}, { "stationID": 2, "value": 50 } ] }'

        json_message = JSONMessage.create(input)
        self.assertFalse(json_message.is_valid())

if __name__ == '__main__':
    unittest.main()