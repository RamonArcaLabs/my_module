from odoo import http
from odoo.http import request
import requests

class MyModule(http.Controller):

    @http.route('/chatbot', auth='user', type='http', website=True)
    def chatbot_page(self, **kwargs):
        return request.render('your_module_name.chatbot_template', {})

    @http.route('/poc', auth='public')
    def add(self, **kw):
        session_id = http.request.httprequest.cookies.get('session_id')
        uid = http.request.session.uid

        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')


        # Construir la URL para el agente
        url = f'http://127.0.0.1:5000/agent-query?query=Dame-las-ventas-mayores-a-10000&session_id={session_id}&uid={uid}&url={base_url}'
        response = requests.get(url)
        return response

    @http.route('/custom_api', type='json', auth='user')
    def get_custom_response(self, query):
        """ Llama a la API externa y devuelve la respuesta """
        try:

            session_id = http.request.httprequest.cookies.get('session_id')
            uid = http.request.session.uid
            base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')

            api_url = f'http://host.docker.internal:5000/agent-query?query={query}&session_id={session_id}&uid={uid}&url={base_url}'

            response = requests.get(api_url)

            if response.headers.get('Content-Type') == 'application/json':
                response_data = response.json()
                message = response_data.get('response', 'Sin respuesta')
            else:
                message = response.text

            return message
        except Exception as e:
            return {'response': str(e)}
