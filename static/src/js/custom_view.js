odoo.define('my_module.CustomView', function(require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var ajax = require('web.ajax');

    var CustomView = AbstractAction.extend({
        template: 'my_module.custom_view',
        
        events: {
            'click #send_prompt': '_onSendPrompt',
        },

        _onSendPrompt: function () {
            var self = this;
            var prompt = this.$('#my_prompt').val();
            
            if (!prompt) {
                this.$('#response').text("Por favor, ingresa un texto.");
                return;
            }

            ajax.jsonRpc('/custom_api', 'call', { query: prompt })
                .then(function(result) {
                    self.$('#response').text(result.response);
                })
                .catch(function(error) {
                    self.$('#response').text("Error al obtener respuesta.");
                });
        }
    });

    core.action_registry.add('custom_view_action', CustomView);
});
