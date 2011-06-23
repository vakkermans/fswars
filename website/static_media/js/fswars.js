this.fswars = {};

this.fswars.add_notification = function(message) {
    this.add_message('<em>'+message+'</em>');
}

this.fswars.add_chat = function(message) {
    this.add_message(message);
}

this.fswars.add_message = function(message) {
    $('#comet_incoming').append(message+'<br>');
    this.toBottom();
}

this.fswars.toBottom = function () {
    $('#comet_incoming').attr('scrollTop', $('#comet_incoming').attr('scrollHeight'));
}

this.fswars.displaySoundInfo = function(sound, addButton, removeButton, addHandlersFunction, appendSelector) {
    var tags = sound.properties['tags'].slice(0,15).join('</span> <span class="tags">');

    var soundHTML = '';

    soundHTML += '<div class="sound sound_'+sound.properties['id']+'">';
    if (removeButton) {
        soundHTML += 	'<div class="sound_remove"><img src="/static_media/images/tab_left.png" /></div>';
    }

    soundHTML +=	'<div class="player small">';
    soundHTML +=	   	'<div class="metadata">'
    soundHTML += 			 sound.properties['preview-hq-mp3'] + ' ';
    soundHTML +=			 sound.properties['waveform_m'] + ' ';
    soundHTML +=			 sound.properties['spectral_m'] + ' ';
    soundHTML +=			 sound.properties['duration'];
    soundHTML +=		'</div>';
    soundHTML +=	'</div>';
    soundHTML += 	'<div class="sound_description">';
    soundHTML +=    	'<span class="sound_title">' + sound.properties.original_filename + '</span><br>';
    soundHTML +=    	'<span class="tags">' + tags + '</span>';
    soundHTML +=    '</div>';
    if (addButton) {
        soundHTML += 	'<div class="sound_add"><img src="/static_media/images/tab_right.png" /></div>';
    }
    soundHTML +=    '<br style="clear: both;">';
    soundHTML += '</div>';

    $(appendSelector).append(soundHTML);

    var selector = appendSelector + ' .sound_'+sound.properties['id'];
    addHandlersFunction($(selector), sound.properties['id']);
    makePlayer(selector + ' .player');
}

this.fswars.activate_waiting_screen = function(message) {
    $('#loading_animation').css('visibility', 'visible');
    $('#game_status_line').text(message);
    $('#game_status_line').show(200);
    $('#waiting_screen').show(200);
    $('#waiting_screen').css('zIndex', 200);
}

this.fswars.deactivate_waiting_screen = function() {
    $('#loading_animation').css('visibility', 'hidden');
    $('#game_status_line').hide(200);
    $('#game_status_line').text('');
    $('#waiting_screen').hide(200);
    $('#waiting_screen').css('zIndex', -200);
}

this.fswars.initialize_waiting_screen = function() {
    $('#loading_animation').css('visibility', 'hidden');
    $('#game_status_line').hide();
    $('#waiting_screen').hide();
}

this.fswars.browser2browser = function(battleId, data) {
    $.post('/battle/'+battleId+'/browser2browser/',
           {message: JSON.stringify(data)});
}
