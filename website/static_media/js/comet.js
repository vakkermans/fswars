(function($)
{
    var cometd = $.cometd;

    $(document).ready(function()
    {
        // set up comet
        if(config.battleId != null) {
            function _connectionEstablished()
            {
                $('#comet_status').html('Connection Established');
                // request battle info, to not lose any data
                $.get('/battle/'+config.battleId+'/request-battle-status/');
            }

            function _connectionBroken()
            {
                $('#comet_status').html('Connection Broken');
            }

            function _connectionClosed()
            {
                $('#comet_status').html('Connection Closed');
            }

            // Function that manages the connection status with the Bayeux server
            var _connected = false;
            function _metaConnect(message)
            {
                if (cometd.isDisconnected())
                {
                    _connected = false;
                    _connectionClosed();
                    return;
                }

                var wasConnected = _connected;
                _connected = message.successful === true;
                if (!wasConnected && _connected)
                {
                    _connectionEstablished();
                }
                else if (wasConnected && !_connected)
                {
                    _connectionBroken();
                }
            }

            function _page_comet_handler_helper(m) {
                console.debug(m);
                var command = jQuery.parseJSON(m.data.command);
                console.debug(command);
                if (command.command == 'updateChat') {
                    fswars.add_chat(command.message);
                } else {
                    page_comet_handler(command);
                }
            }

            // Function invoked when first contacting the server and
            // when the server has lost the state of this client
            function _metaHandshake(handshake)
            {
                if (handshake.successful === true) {
                    cometd.batch(function() {
                        cometd.subscribe('/updates', _page_comet_handler_helper);
                        // Publish on a service channel since the message is for the server only
                        cometd.publish('/service/updates', { battle_id: config.battleId });
                    });
                }
            }

            // Disconnect when the page unloads
            $(window).unload(function()
            {
                cometd.disconnect(true);
            });

            cometd.configure({
                url: cometURL,
                logLevel: 'info'
            });

            cometd.addListener('/meta/handshake', _metaHandshake);
            cometd.addListener('/meta/connect', _metaConnect);

            cometd.handshake();
        }
    });
})(jQuery);
