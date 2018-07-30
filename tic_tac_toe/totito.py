import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import aiy.i18n

import tic_tac_toe
from tic_tac_toe import Environment
from tic_tac_toe import Agent
from tic_tac_toe import Human

from time import sleep
import pickle
import requests
import json
endpoint_url ="https://firestore.googleapis.com/v1beta1/projects/alphatotito/databases/(default)/documents/board_state/current_state"


human = Human()
env = Environment()
human.set_symbol(env.o)
LENGTH = 3


aiy.i18n.set_language_code("es-ES")

def play_game(player1,player2,env,draw= False):
    # game loop until game over
	current_player = None	
	while not env.game_over():
        # alternate between players ,p1 always starts first
		if current_player == player1:
			current_player = player2
		else:
			current_player = player1
            
		if draw:
 			if (draw == 1 and current_player == player1) or (draw == 2 and current_player == 2):
 				env.draw_board()
                
		current_player.take_action(env)

		state = env.get_state()
		player1.update_state_history(state)
		player2.update_state_history(state)
        
		if draw:
			env.draw_board()
        
        
	player1.update(env)
	player2.update(env)

def train(GAMES_TO_PLAY):
	p1 = Agent()
	p2 = Agent()

  	# set initial V for p1 and p2
	env = Environment()
	state_winner_triples = tic_tac_toe.get_state_hash_and_winner(env)


	Vx = tic_tac_toe.initialV_x(env, state_winner_triples)
	p1.setV(Vx)
	Vo = tic_tac_toe.initialV_o(env, state_winner_triples)
	p2.setV(Vo)

  # give each player their symbol
	p1.set_symbol(env.x)
	p2.set_symbol(env.o)

	for t in range(GAMES_TO_PLAY):
    
        
 		print("starting train game ",t)
 		play_game(p1,p2,Environment(),draw=False)
	

	with open("player1_{}.pkl".format(LENGTH),"wb") as p1_dump:
		pickle.dump(p1,p1_dump,pickle.HIGHEST_PROTOCOL)

	return p1,p2

word_to_num = {
			#'cero':0,
			'uno':1,
			'dos':2 ,
			 'tres':3 } #,

ordinal_to_num = {
			"primera":1,
			"segunda":2,
			"tercera":3
}
			 # "cuatro":4,
			  #"cinco":5}

def identify_selection(text):

	if text is None:
		return 0
	elif len(text) == 0 :
		return 0

	text = text.lower()

	for num in word_to_num.keys():
		if num in text or str(word_to_num[num]) in text:
			return word_to_num[num] 


	for num in ordinal_to_num.keys():
		if num in text or str(ordinal_to_num[num]) in text:
			return ordinal_to_num[num] 

	return 0

def say_election(row_num=1,col_num=1):
	aiy.audio.say("yo elijo: fila {}, columna {}".format(row_num,col_num))
	
def say_your_turn(player_name = "humano"):
	aiy.audio.say("Tu turno: {}".format(player_name))


def get_agent_action():
	row = 0
	column = 0
	
	return row,column


def main():
	recognizer = aiy.cloudspeech.get_recognizer()

	for num in word_to_num.keys():
		recognizer.expect_phrase(num)
		recognizer.expect_phrase(str(word_to_num[num]))
		recognizer.expect_phrase("columna "+num)
		recognizer.expect_phrase("columna "+str(word_to_num[num]))
		recognizer.expect_phrase("fila "+num)
		recognizer.expect_phrase("fila "+str(word_to_num[num]))
		recognizer.expect_phrase("elijo "+num)
		recognizer.expect_phrase("elijo "+str(word_to_num[num]))
		recognizer.expect_phrase("elijo fila "+num)
		recognizer.expect_phrase("elijo fila "+str(word_to_num[num]))
		recognizer.expect_phrase("elijo columna "+num)
		recognizer.expect_phrase("elijo columna "+str(word_to_num[num]))

	for num in ordinal_to_num.keys():
		recognizer.expect_phrase(num)
		recognizer.expect_phrase(str(ordinal_to_num[num]))
		recognizer.expect_phrase("columna "+num)
		recognizer.expect_phrase("columna "+str(ordinal_to_num[num]))
		recognizer.expect_phrase("fila "+num)
		recognizer.expect_phrase("fila "+str(ordinal_to_num[num]))
		recognizer.expect_phrase("elijo "+num)
		recognizer.expect_phrase("elijo "+str(ordinal_to_num[num]))
		recognizer.expect_phrase("elijo fila "+num)
		recognizer.expect_phrase("elijo fila "+str(ordinal_to_num[num]))
		recognizer.expect_phrase("elijo columna "+num)
		recognizer.expect_phrase("elijo columna "+str(ordinal_to_num[num]))
		
		
	recognizer.expect_phrase("terminar juego")
	recognizer.expect_phrase("finalizar juego")
	recognizer.expect_phrase("entrenar")
	recognizer.expect_phrase("jugar")

	button = aiy.voicehat.get_button()
	led = aiy.voicehat.get_led()
	aiy.audio.get_recorder().start()
	
	aiy.audio.say("Selecciona jugar o entrenar")
	text = recognizer.recognize().lower()

	if "entrenar" in text:
		aiy.audio.say("Ok, entrenando agente")
		p1,p2 = train(10)
		print("Finished training ",p1,p2)
	elif "jugar" in text:
		with open("player1_{}.pkl".format(LENGTH),"rb") as p1_dump:
			p1 = pickle.load(p1_dump)
	else:
		aiy.audio.say("Opción no valida")
		return

	FINISH_GAME = False
	iterations = 0

	while not FINISH_GAME: 
		if iterations > 0:
			aiy.audio.say("Desea jugar o salir?")
			election = recognizer.recognize()

			if "salir" in election or "terminar" in election or "finalizar" in election or "quitar" in election:
				FINISH_GAME = True 
				continue
			elif not "jugar" in election:
				aiy.audio.say("Opcion no valida, seleccionar jugar o salir")
				continue
			elif "jugar" in election:
				print("Start game")

		aiy.audio.say("Empezando el juego")
		aiy.audio.say("Cual es tu nombre?")
		recognized_name = recognizer.recognize()
		player_name = "humano"

		if not recognized_name is None:
			if len(recognized_name) > 0:
				player_name = recognized_name 

		turn = "human"
		
		GAME_OVER = False
		env = Environment()
		env.draw_board()

		while not GAME_OVER:
			

			if turn == "human":
				row = -1
				col = -1
				say_your_turn(player_name)
				aiy.audio.say("Que fila elijes?")
				text = recognizer.recognize()
				print("Dijiste ",text)
			
				if text is None:
					continue

				if "terminar" in text or "finalizar" in text or "salir" in text:
					aiy.audio.say("Ok, hasta luego!")
					break
				
				row = identify_selection(text) -1
					
				aiy.audio.say("Que columna elijes?")
				text = recognizer.recognize()
				print("Dijiste ",text)
				
				if text is None:
					continue

				if "terminar" in text or "finalizar" in text or "salir" in text:
					aiy.audio.say("Ok, hasta luego!")
					break

				col = identify_selection(text) -1
					
				print("Elegiste fila {} columna {}".format(str(row+1),str(col+1)))

				if row == -1 or col == -1 or not env.is_empty(row,col):
					aiy.audio.say("Elección no valida")
					continue

				human.do_action(env,row,col)
				execute_ui_endpoint(env)
				turn = "agent"
				env.draw_board()
				sleep(1.0)

				GAME_OVER = env.game_over() 
				
				if GAME_OVER and env.winner == human.sym:
					aiy.audio.say("Felicitaciones, ganaste")
				
			else:
				new_state = p1.take_action(env)
				
				num_state = env.get_state()
				say_election(new_state[1]+1,new_state[2]+1)
				sleep(0.5)

				print(new_state)
				env.draw_board()
				execute_ui_endpoint(env)
				
				GAME_OVER = env.game_over()
				
				if GAME_OVER and env.winner == p1.sym:
					aiy.audio.say("Lo siento, yo gano. ja ja")
				turn = "human"

			if env.ended and env.winner == None:
				GAME_OVER = True
				aiy.audio.say("Es un empate")
		iterations+=1

def calculate_ui_endpoint(env):
	request_string = """{
  					"name": "projects/alphatotito/databases/(default)/documents/board_state/current_state",
					  "fields": {
					    "state": {
					      "integerValue": """ + str(env.get_state())+ """
					    },
					    "board": {
					      "arrayValue": {
					        "values": ["""
	board_values = ""
	for i in range(LENGTH):
		for j in range(LENGTH):
			board_values+='{"integerValue":"'+str(int(env.board[i][j]))+'"},'

	board_values= board_values[0:-1]

	request_string +=board_values+"""]
      	}
    	}
  		},
  		"createTime": "2018-07-26T05:24:12.163712Z",
  		"updateTime": "2018-07-30T05:11:21.532238Z"
		}"""

	return request_string

def execute_ui_endpoint(env):
	payload = calculate_ui_endpoint(env)

	return requests.request("patch",endpoint_url,data = payload)

if __name__ == "__main__":
	main()
