// Javascript class reflecting Python battle object
function battle_model() {
	
	//------------ members
	this.id;
	this.player1;
	this.player1_uuid;
	this.player2;
	this.player2_uuid;
	this.player1_sounds;
	this.player2_sounds;
	this.num_rounds;
	this.turn_owner;
	this.finished;
	
	//------ Initialize all variables (like constructor...)
	this.init = function init(jsonBattle) {
		this.id				= jsonBattle['id']
		this.player1 		= jsonBattle['fields']['player1'];
		this.player1_uuid 	= jsonBattle['fields']['player1_uuid'];
		this.player2 		= jsonBattle['fields']['player2'];
		this.player2_uuid   = jsonBattle['fields']['player2_uuid'];
		this.player1_sounds = jsonBattle['fields']['player1_sounds'];
		this.player2_sounds = jsonBattle['fields']['player2_sounds'];
		this.num_rounds		= jsonBattle['fields']['num_rounds'];
		this.turn_owner		= jsonBattle['fields']['turn_owner'];
		this.finished		= jsonBattle['fields']['finished'];
	}
}