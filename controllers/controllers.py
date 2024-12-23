# -*- coding: utf-8 -*-
from odoo import http
import requests
import json


class MyModule(http.Controller):
    @http.route('/hi', auth='public')
    def index(self, **kw):
        sale = http.request.env['res.partner'].search([('id', '=', 4798)], limit=1)
        return "Hello, world "

    @http.route('/poc', auth='public')
    def add(self, **kw):
        try:
            session_id = http.request.httprequest.cookies.get('session_id')
            uid = http.request.session.uid

            base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')

            url = f'https://8375-66-9-176-125.ngrok-free.app/agent-query?query=Buscar orden de venta con ID 7&session_id={session_id}&uid={uid}&url={base_url}'

            response = requests.get(url)

            if response.headers.get('Content-Type') == 'application/json':
                response_data = response.json()
            else:
                response_data = {"response": response.text}

            return http.Response(
                json.dumps(response_data),
                content_type='application/json',
                status=200
            )

        except Exception as e:
            return http.Response(
                json.dumps({"error": str(e)}),
                content_type='application/json',
                status=500
            )
