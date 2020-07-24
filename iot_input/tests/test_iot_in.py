from odoo.tests.common import TransactionCase


class TestIotIn(TransactionCase):
    def test_device(self):
        serial = 'testingdeviceserial'
        passphrase = 'password'
        device = self.env['iot.device'].create({
            'name': 'Device',
        })
        device_input = self.env['iot.device.input'].create({
            'name': 'Input',
            'device_id': device.id,
            'active': True,
            'serial': serial,
            'passphrase': passphrase,
            'call_model_id': self.ref('iot_input.model_iot_device_input'),
            'call_function': 'test_input_device'
        })
        iot = self.env['iot.device.input']
        self.assertFalse(
            iot.get_device(serial=serial + serial, passphrase=passphrase))
        self.assertFalse(
            iot.get_device(serial=serial, passphrase=passphrase + passphrase))
        iot = iot.get_device(
            serial=serial, passphrase=passphrase)
        self.assertEqual(iot, device_input)
        args = 'hello'
        res = iot.call_device(args)
        self.assertEqual(res, {'status': 'ok', 'value': args})
        self.assertTrue(device_input.action_ids)
        self.assertEqual(device_input.action_ids.args, str(args))
        self.assertEqual(device_input.action_ids.res, str(res))

        value = '12'
        response1 = iot.get_device_input(serial=serial + serial,
                                         passphrase=passphrase,
                                         value=value)
        self.assertEqual(response1['status'], 'error')

        response2 = iot.get_device_input(serial=serial,
                                         passphrase=passphrase + passphrase,
                                         value=value)
        self.assertEqual(response2['status'], 'error')

        device_input.call_function = 'test_model_function'
        response3 = iot.get_device_input(
            serial=serial, passphrase=passphrase, value=value)
        self.assertEqual(response3['status'], 'ok')
        self.assertEqual(response3['message'], value)

        device_input.active = False
        response4 = iot.get_device_input(
            serial=serial, passphrase=passphrase, value=value)
        self.assertEqual(response4['status'], 'error')
