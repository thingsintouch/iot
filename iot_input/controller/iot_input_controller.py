# Copyright 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from odoo import http, _
import logging
import traceback
from io import StringIO
logger = logging.getLogger(__name__)


class CallIot(http.Controller):
    @http.route([
        '/iot/<serial>/action',
    ], type='http', auth="none", methods=['POST'], csrf=False)
    def call_unauthorized_iot(self, serial, *args, **kwargs):
        request = http.request
        if not request.env:
            return json.dumps(False)
        return json.dumps(request.env['iot.device.input'].sudo().get_device(
            serial, kwargs['passphrase']).call_device(kwargs['value']))

    @http.route([
        '/iot/<serial>/action2',
    ], type='http', auth="none", methods=['POST'], csrf=False)
    def call_unauthorized_iot_action(self, serial, *args, **kwargs):
        request = http.request
        if not request.env:
            return json.dumps({'status': 'error',
                               'message': _('env not set')})
        try:
            result = request.env['iot.device.input'].sudo().get_device(
            serial, kwargs['passphrase']).call_device(kwargs['value'])
            if 'status' not in result or 'message' not in result:
                result = {
                    'status': 'ok',
                    'message': _('All processed properly'),
                    'result': result,
                }
            return json.dumps(result)
        except Exception:
            request.env.cr.rollback()
            buff = StringIO()
            traceback.print_exc(file=buff)
            logger.error(buff.getvalue())
            return json.dumps({
                "status": "error",
                "message": _('Something went wrong')
            })

    @http.route([
        '/iot/<serial>/check',
    ], type='http', auth="none", methods=['POST'], csrf=False)
    def check_unauthorized_iot(self, serial, *args, **kwargs):
        request = http.request
        if not request.env:
            return json.dumps(False)
        device = request.env['iot.device.input'].sudo().get_device(
            serial, kwargs['passphrase'])
        if device:
            return json.dumps({"state": True})
        return json.dumps({"state": False})
