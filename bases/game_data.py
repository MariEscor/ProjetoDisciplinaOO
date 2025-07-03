#game_data.py
TRAINER_DATA = {
    'wx': {
        'name': 'Leandro, o Colorado',
        'monsters': {
            'poke1': ['starmie', 63],
            'poke2': ['seadra', 65],
            'poke3': ['cloyster', 67]
        },
        'dialog': {
            'default': [
                "Prepare-se para uma enxurrada de ataques!",
                "Vamos ver se você aguenta a pressão."
            ],
            'defeated': [
                "Você nadou melhor do que eu esperava.",
                "Vou treinar mais minhas ondas!"
            ]
        },
        'look_around': False,
        'directions': ['down'],
        'defeated': False
    },
    'fx': {
        'name': 'Pedro, o Discreto',
        'monsters': {
            'poke1': ['ninetales', 63],
            'poke2': ['arcanine', 65],
            'poke3': ['magmar', 67]
        },
        'dialog': {
            'default': [
                "Sinta o calor da batalha!",
                "O fogo purifica os fracos!"
            ],
            'defeated': [
                "Você apagou minha chama...",
                "Mas o fogo sempre volta a queimar!"
            ]
        },
        'look_around': True,
        'directions': ['down'],
        'defeated': False
    },
    'px': {
        'name': 'Adriana, a Mapeadora',
        'monsters': {
            'poke1': ['vileplume', 63],
            'poke2': ['tangela', 65],
            'poke3': ['exeggutor', 67]
        },
        'dialog': {
            'default': [
                "A beleza das plantas pode ser perigosa!",
                "Cuidado, espinhos à frente!"
            ],
            'defeated': [
                "Você podou minha estratégia.",
                "As folhas caem... mas voltam a crescer."
            ]
        },
        'look_around': False,
        'directions': ['down'],
        'defeated': False
    },
	'Nurse': {
		'direction': 'down',
		'radius': 0,
		'look_around': False,
		'dialog': {
			'default': ['Bem vindo, cada cura equivale a 1 ponto na media', 'TA TODO MUNDO CURADO!'], 
			'defeated': None},
		'directions': ['down'],
		'defeated': False,
		'biome': None
		}
}


''''ox': {
        'name': 'Rodrigo e Larissa, a Dupla Dinâmica',
        'monsters': {
            'poke1': ['spiritomb', 67],
            'poke2': ['milotic', 70],
            'poke3': ['garchomp', 73]
        },
        'dialog': {
            'default': [
                "O futuro da sua derrota já foi previsto.",
                "Nada escapa ao nosso sexto sentido."
            ],
            'defeated': [
                "Nossas visões estavam erradas...",
                "Mas voltaremos mais poderosos!"
            ]
        },
        'look_around': False,
        'directions': ['down'],
        'defeated': False
},'''