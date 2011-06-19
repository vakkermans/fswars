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
