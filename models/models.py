# -*- coding: utf-8 -*-
from odoo import models, fields, api, http
from odoo.http import request
import requests
import json

class MyModule(models.Model):
    _name = 'my_module.my_module'
    _description = "My Module Model"

    text = fields.Char(string="Prompt")
    output = fields.Char(string="Respuesta", readonly=True)

    def action_api(self):
        """ Envía el prompt a una API externa y muestra la respuesta """
        prompt = self.text
    
        try:
            session_id = http.request.httprequest.cookies.get('session_id')
            uid = http.request.session.uid
            base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')

            api_url = f'http://host.docker.internal:5000/agent-query?query={prompt}&session_id={session_id}&uid={uid}&url={base_url}'

            response = requests.get(api_url)

            if response.headers.get('Content-Type') == 'application/json':
                response_data = response.json()
                message = response_data.get('response', 'Sin respuesta')
            else:
                message = response.text

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Respuesta',
                    'message': message,
                    'sticky': False,
                },
            }

        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': str(e),
                    'sticky': False,
                },
            }