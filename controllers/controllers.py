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
            url = f'https://8153-66-9-176-235.ngrok-free.app/agent-query?query=Buscar producto con ID 22&session_id={session_id}'

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
