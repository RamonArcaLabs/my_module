# -*- coding: utf-8 -*-
from odoo import http
import requests
import json

class MyModule(http.Controller):
    @http.route('/hi', auth='public')
    def index(self, **kw):
        sale = http.request.env['res.partner'].search([('id','=',4798)], limit=1)
        return "Hello, world "

    @http.route('/poc', auth='public')
    def add(self, **kw):
        try:
            session_id = http.request.httprequest.cookies.get('session_id')
            url = 'api_url_here?SessionID='+session_id
            response = requests.get(url)
            response_data = response.json()

            return http.Response(
                    json.dumps(response_data),
                    content_type='application/json',
                    status=200
                )

        except Exception as e:
            return {'error': str(e)}